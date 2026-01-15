"""Base class for social media scrapers with image caching support.

This module provides common functionality for social media scrapers including:
- Image caching by post ID
- Metadata extraction from images
- Anti-scraping measures (delays, realistic headers)
- Reusable OCR integration
"""

from typing import Dict, Any, List, Optional
from pathlib import Path
import time
from ...base import BaseSource, SourceOptions

try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False

try:
    from ...image_analyzer import ImageAnalyzer
    IMAGE_ANALYZER_AVAILABLE = True
except ImportError:
    IMAGE_ANALYZER_AVAILABLE = False


class BaseSocialMediaSource(BaseSource):
    """Base class for social media scrapers with image caching.
    
    Provides common functionality:
    - Image caching by post ID to avoid re-downloading
    - Metadata extraction (alt text, captions, titles)
    - Anti-scraping measures (delays, realistic headers)
    - OCR integration for flyer analysis
    """
    
    # Platform name (override in subclass)
    PLATFORM_NAME = "social_media"
    
    def __init__(self, source_config: Dict[str, Any], options: SourceOptions,
                 base_path: Optional[Path] = None,
                 ai_providers: Optional[Dict[str, Any]] = None):
        super().__init__(source_config, options, base_path=base_path, ai_providers=ai_providers)
        
        self.available = REQUESTS_AVAILABLE
        self.request_delay = 2  # seconds between requests
        self.request_timeout = 15  # request timeout
        
        if self.available:
            self._init_session()
        
        # Initialize image analyzer for OCR
        self._init_image_analyzer(ai_providers)
    
    def _init_session(self):
        """Initialize HTTP session with anti-scraping headers."""
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9,de;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Cache-Control': 'max-age=0'
        })
    
    def _init_image_analyzer(self, ai_providers: Optional[Dict[str, Any]] = None):
        """Initialize image analyzer for OCR."""
        self.image_analyzer = None
        if IMAGE_ANALYZER_AVAILABLE:
            try:
                img_config = {
                    'ocr_enabled': True,
                    'languages': ['eng', 'deu']
                }
                self.image_analyzer = ImageAnalyzer(img_config, ai_providers=ai_providers)
            except Exception as e:
                print(f"    ⚠ Image analyzer init failed: {e}")
    
    def _make_request(self, url: str, delay: bool = True) -> Optional['requests.Response']:
        """Make HTTP request with anti-scraping measures.
        
        Args:
            url: URL to fetch
            delay: Whether to add delay before request (default True)
            
        Returns:
            Response object or None on error
        """
        if delay and self.request_delay > 0:
            time.sleep(self.request_delay)
        
        try:
            response = self.session.get(url, timeout=self.request_timeout)
            response.raise_for_status()
            return response
        except Exception as e:
            print(f"      Request error: {e}")
            return None
    
    def _get_image_cache_dir(self) -> Optional[Path]:
        """Get platform-specific image cache directory.
        
        Returns:
            Cache directory path or None if base_path not set
        """
        if not self.base_path:
            return None
        
        cache_dir = self.base_path / "data" / "image_cache" / self.PLATFORM_NAME
        cache_dir.mkdir(parents=True, exist_ok=True)
        return cache_dir
    
    def _analyze_post_images(self, image_urls: List[str], post_id: Optional[str] = None,
                            image_metadata: Optional[List[Dict[str, str]]] = None) -> Optional[Dict[str, Any]]:
        """Analyze post images for event content using OCR with caching.
        
        Images are cached by post_id to avoid re-downloading and re-processing.
        Image metadata (alt text, captions) is incorporated into OCR results.
        
        Args:
            image_urls: List of image URLs
            post_id: Optional post ID for caching images
            image_metadata: Optional list of metadata dicts (alt, title, aria_label, etc.)
            
        Returns:
            Best event data extracted from images or None
        """
        if not self.image_analyzer:
            return None
        
        # Get cache directory
        image_cache_dir = self._get_image_cache_dir()
        
        best_result = None
        best_confidence = 0.0
        
        for idx, url in enumerate(image_urls[:3]):  # Limit to first 3 images
            try:
                # Get metadata for this image if available
                metadata = None
                if image_metadata and idx < len(image_metadata):
                    metadata = image_metadata[idx]
                
                # Check if we have a cached version of this image
                cached_image_path = None
                if image_cache_dir and post_id:
                    cached_image_path = image_cache_dir / f"{post_id}_{idx}.jpg"
                    if cached_image_path.exists():
                        # Use cached image
                        result = self.image_analyzer.analyze(str(cached_image_path))
                        if result:
                            # Enhance with metadata
                            result = self._enhance_ocr_with_metadata(result, metadata)
                            if result.get('ocr_confidence', 0) > best_confidence:
                                best_confidence = result.get('ocr_confidence', 0)
                                best_result = result
                        continue
                
                # Download and analyze new image
                result = self.image_analyzer.analyze_url(url, timeout=10)
                if result:
                    # Enhance with metadata
                    result = self._enhance_ocr_with_metadata(result, metadata)
                    if result.get('ocr_confidence', 0) > best_confidence:
                        best_confidence = result.get('ocr_confidence', 0)
                        best_result = result
                        
                        # Cache the image for future use
                        if cached_image_path:
                            try:
                                response = self._make_request(url, delay=False)
                                if response:
                                    cached_image_path.write_bytes(response.content)
                            except Exception as e:
                                print(f"      Failed to cache image: {e}")
                                
            except Exception as e:
                print(f"      OCR analysis error: {e}")
                continue
        
        # Only return if confidence is above threshold (configurable, default 0.3)
        min_confidence = getattr(self, 'min_ocr_confidence', 0.3)
        if best_result and best_confidence >= min_confidence:
            return best_result
        
        return None
    
    def _enhance_ocr_with_metadata(self, ocr_result: Dict[str, Any], 
                                  metadata: Optional[Dict[str, str]]) -> Dict[str, Any]:
        """Enhance OCR results with image metadata.
        
        Combines OCR text with alt text, captions, titles to get fuller picture.
        
        Args:
            ocr_result: OCR analysis result
            metadata: Image metadata (alt, title, aria_label, caption)
            
        Returns:
            Enhanced OCR result
        """
        if not metadata:
            return ocr_result
        
        # Collect all metadata text
        metadata_text = []
        for key in ['alt', 'title', 'aria_label', 'caption']:
            if metadata.get(key):
                metadata_text.append(metadata[key])
        
        # Append metadata to OCR text
        if metadata_text:
            combined_text = ocr_result.get('text', '')
            if combined_text:
                combined_text += '\n' + '\n'.join(metadata_text)
            else:
                combined_text = '\n'.join(metadata_text)
            
            ocr_result['text'] = combined_text
            ocr_result['has_metadata'] = True
        
        return ocr_result
    
    def extract_image_metadata(self, img_element) -> Dict[str, str]:
        """Extract metadata from image HTML element.
        
        Args:
            img_element: BeautifulSoup image element
            
        Returns:
            Dictionary with alt, title, aria_label, etc.
        """
        return {
            'url': img_element.get('src', '') or img_element.get('data-src', ''),
            'alt': img_element.get('alt', ''),
            'title': img_element.get('title', ''),
            'aria_label': img_element.get('aria-label', '')
        }
