"""Custom scraper for Hof Stadt website events."""

from typing import Dict, Any, List, Optional
from datetime import datetime
from urllib.parse import urljoin
from pathlib import Path
from ...base import BaseSource, SourceOptions
from .date_utils import extract_date_from_text, generate_stable_event_id

try:
    import requests
    from bs4 import BeautifulSoup
    SCRAPING_AVAILABLE = True
except ImportError:
    SCRAPING_AVAILABLE = False


class HofStadtSource(BaseSource):
    """
    Custom scraper for Hof Stadt website event listings.
    
    The official Hof city website (www.hof.de) hosts various event
    announcements including the weekly market and other community events.
    """
    
    def __init__(self, source_config: Dict[str, Any], options: SourceOptions,
                 base_path: Optional[Path] = None, ai_providers: Optional[Dict[str, Any]] = None):
        super().__init__(
            source_config,
            options,
            base_path=base_path,
            ai_providers=ai_providers
        )
        self.available = SCRAPING_AVAILABLE
        
        if self.available:
            self.session = requests.Session()
            self.session.headers.update({
                'User-Agent': (
                    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                    'AppleWebKit/537.36 (KHTML, like Gecko) '
                    'Chrome/120.0.0.0 Safari/537.36'
                )
            })
    
    def scrape(self) -> List[Dict[str, Any]]:
        """Scrape events from Hof Stadt website."""
        if not self.available:
            print("  ⚠ Requests/BeautifulSoup not available")
            return []
        
        events = []
        try:
            response = self.session.get(self.url, timeout=15)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'lxml')
            
            # Look for event containers on Hof Stadt website
            event_containers = (
                soup.select('.veranstaltung') or
                soup.select('.event') or
                soup.select('article') or
                soup.select('.termin') or
                soup.select('.item')[:20]  # Fallback
            )
            
            if not event_containers:
                print(f"    No events found on page")
                return []
            
            print(f"    Found {len(event_containers)} potential events")
            
            for i, container in enumerate(event_containers[:20], 1):
                try:
                    event = self._parse_event(container)
                    if event and not self.filter_event(event):
                        events.append(event)
                        print(f"    [{i}/{min(len(event_containers), 20)}] ✓ {event['title'][:50]}")
                except Exception as e:
                    print(f"    [{i}] ✗ Parse error: {str(e)[:50]}")
                    
        except requests.exceptions.RequestException as e:
            print(f"    Request error: {str(e)}")
        except Exception as e:
            print(f"    Scraping error: {str(e)}")
        
        return events
    
    def _parse_event(self, container) -> Optional[Dict[str, Any]]:
        """Parse event from HTML container."""
        # Extract title
        title_elem = container.find(['h1', 'h2', 'h3', 'h4', 'a', 'strong'])
        if not title_elem:
            return None
        title = title_elem.get_text(strip=True)
        
        if not title or len(title) < 3:
            return None
        
        # Extract description
        desc_elem = container.find(['p', '.description', '.text', 'div'])
        description = desc_elem.get_text(strip=True)[:500] if desc_elem else ''
        
        # Extract URL
        link_elem = container.find('a', href=True)
        event_url = urljoin(self.url, link_elem['href']) if link_elem else self.url
        
        # Extract date using shared utility  
        date_text = container.get_text()
        start_time = extract_date_from_text(date_text, default_hour=10)
        
        # Use default location
        location = self.options.default_location or {
            'name': 'Hof',
            'lat': 50.3167,
            'lon': 11.9167
        }
        
        return {
            'id': generate_stable_event_id('hofstadt', title, start_time),
            'title': title[:200],
            'description': description,
            'location': location,
            'start_time': start_time,
            'end_time': None,
            'url': event_url,
            'source': self.name,
            'category': self.options.category or 'community',
            'scraped_at': datetime.now().isoformat(),
            'status': 'pending'
        }
