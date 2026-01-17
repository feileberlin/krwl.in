"""Custom scraper for VHS Hofer Land (Volkshochschule)."""

from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
from urllib.parse import urljoin
import re
from pathlib import Path
from ...base import BaseSource, SourceOptions

try:
    import requests
    from bs4 import BeautifulSoup
    SCRAPING_AVAILABLE = True
except ImportError:
    SCRAPING_AVAILABLE = False


class VHSSource(BaseSource):
    """
    Custom scraper for VHS Hofer Land last-minute courses.
    
    VHS (Volkshochschule) is an adult education center offering various
    courses and workshops. This scraper focuses on last-minute course offerings.
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
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            })
    
    def scrape(self) -> List[Dict[str, Any]]:
        """Scrape courses from VHS."""
        if not self.available:
            print("  ⚠ Requests/BeautifulSoup not available")
            return []
        
        events = []
        try:
            response = self.session.get(self.url, timeout=15)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'lxml')
            
            # Look for course containers
            # VHS sites often use table layouts or list items for courses
            course_containers = (
                soup.select('.course-item') or
                soup.select('.kurs') or
                soup.select('tr[class*="course"]') or
                soup.select('li[class*="course"]') or
                soup.select('article') or
                soup.select('.item')[:20]  # Fallback
            )
            
            if not course_containers:
                print(f"    No courses found on page")
                return []
            
            print(f"    Found {len(course_containers)} potential courses")
            
            for i, container in enumerate(course_containers[:20], 1):
                try:
                    event = self._parse_course(container)
                    if event and not self.filter_event(event):
                        events.append(event)
                        print(f"    [{i}/{min(len(course_containers), 20)}] ✓ {event['title'][:50]}")
                except Exception as e:
                    print(f"    [{i}] ✗ Parse error: {str(e)[:50]}")
                    
        except requests.exceptions.RequestException as e:
            print(f"    Request error: {str(e)}")
        except Exception as e:
            print(f"    Scraping error: {str(e)}")
        
        return events
    
    def _parse_course(self, container) -> Optional[Dict[str, Any]]:
        """Parse course from HTML container."""
        # Extract title
        title_elem = container.find(['h1', 'h2', 'h3', 'h4', 'a', 'strong'])
        if not title_elem:
            return None
        title = title_elem.get_text(strip=True)
        
        if not title or len(title) < 5:
            return None
        
        # Skip if it's just a header
        if title.lower() in ['kurse', 'veranstaltungen', 'termine']:
            return None
        
        # Extract description
        desc_elem = container.find(['p', '.description', 'td'])
        description = desc_elem.get_text(strip=True)[:500] if desc_elem else ''
        
        # Extract URL
        link_elem = container.find('a', href=True)
        event_url = urljoin(self.url, link_elem['href']) if link_elem else self.url
        
        # Extract date
        date_text = container.get_text()
        start_time = self._extract_date(date_text)
        
        # Use default location
        location = self.options.default_location or {
            'name': 'VHS Hofer Land',
            'lat': 50.3167,
            'lon': 11.9167
        }
        
        return {
            'id': f"vhs_{hash(title + start_time)}",
            'title': title[:200],
            'description': description,
            'location': location,
            'start_time': start_time,
            'end_time': None,
            'url': event_url,
            'source': self.name,
            'category': self.options.category or 'education',
            'scraped_at': datetime.now().isoformat(),
            'status': 'pending'
        }
    
    def _extract_date(self, text: str) -> str:
        """Extract date from text using German date patterns."""
        # Look for common German date formats
        patterns = [
            (r'(\d{1,2})\.(\d{1,2})\.(\d{4})', 'DMY'),  # DD.MM.YYYY
            (r'(\d{1,2})\.(\d{1,2})\.(\d{2})', 'DMY_SHORT'),  # DD.MM.YY
            (r'(\d{4})-(\d{2})-(\d{2})', 'YMD'),  # YYYY-MM-DD
            (r'ab\s+(\d{1,2})\.(\d{1,2})\.(\d{4})', 'DMY'),  # ab DD.MM.YYYY
        ]
        
        for pattern, format_type in patterns:
            match = re.search(pattern, text)
            if match:
                try:
                    groups = match.groups()
                    if format_type == 'DMY':
                        day, month, year = groups[-3:]
                        date = datetime(int(year), int(month), int(day), 18, 0)
                    elif format_type == 'DMY_SHORT':
                        day, month, year = groups[-3:]
                        year = int('20' + year) if int(year) < 50 else int('19' + year)
                        date = datetime(year, int(month), int(day), 18, 0)
                    elif format_type == 'YMD':
                        year, month, day = groups[-3:]
                        date = datetime(int(year), int(month), int(day), 18, 0)
                    
                    # Only return dates in the future
                    if date > datetime.now():
                        return date.isoformat()
                except (ValueError, TypeError):
                    continue
        
        # Default to next week if no valid date found
        return (datetime.now() + timedelta(days=7)).replace(hour=18, minute=0).isoformat()
