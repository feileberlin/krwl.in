"""Custom scraper for Freiheitshalle Hof event venue."""

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


class FreiheitshalleSource(BaseSource):
    """
    Custom scraper for Freiheitshalle Hof.
    
    Freiheitshalle is a major cultural center in Hof with concerts, theater,
    and other performances. The scraper extracts events from their event listing page.
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
        """Scrape events from Freiheitshalle."""
        if not self.available:
            print("  ⚠ Requests/BeautifulSoup not available")
            return []
        
        events = []
        try:
            response = self.session.get(self.url, timeout=15)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'lxml')
            
            # Look for event containers
            # Try multiple selectors in order of specificity
            event_containers = (
                soup.select('.event-item') or
                soup.select('.veranstaltung') or
                soup.select('article.event') or
                soup.select('.event-list .item') or
                soup.select('[class*="event"]')[:20]  # Fallback, limit to 20
            )
            
            if not event_containers:
                print(f"    No events found on page")
                return []
            
            print(f"    Found {len(event_containers)} potential events")
            
            for i, container in enumerate(event_containers[:20], 1):  # Limit to 20
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
        title_elem = container.find(['h1', 'h2', 'h3', 'h4', 'a'])
        if not title_elem:
            return None
        title = title_elem.get_text(strip=True)
        
        if not title or len(title) < 3:
            return None
        
        # Extract description
        desc_elem = container.find(['p', '.description', '.text'])
        description = desc_elem.get_text(strip=True)[:500] if desc_elem else ''
        
        # Extract URL
        link_elem = container.find('a', href=True)
        event_url = urljoin(self.url, link_elem['href']) if link_elem else self.url
        
        # Extract date
        date_text = container.get_text()
        start_time = self._extract_date(date_text)
        
        # Use default location
        location = self.options.default_location or {
            'name': 'Freiheitshalle Hof',
            'lat': 50.3191,
            'lon': 11.9173
        }
        
        return {
            'id': f"freiheitshalle_{hash(title + start_time)}",
            'title': title[:200],
            'description': description,
            'location': location,
            'start_time': start_time,
            'end_time': None,
            'url': event_url,
            'source': self.name,
            'category': self.options.category or 'culture',
            'scraped_at': datetime.now().isoformat(),
            'status': 'pending'
        }
    
    def _extract_date(self, text: str) -> str:
        """Extract date from text using German date patterns."""
        # Look for DD.MM.YYYY or DD.MM.YY patterns
        patterns = [
            (r'(\d{1,2})\.(\d{1,2})\.(\d{4})', 'DMY'),  # DD.MM.YYYY
            (r'(\d{1,2})\.(\d{1,2})\.(\d{2})', 'DMY_SHORT'),  # DD.MM.YY
            (r'(\d{4})-(\d{2})-(\d{2})', 'YMD'),  # YYYY-MM-DD
        ]
        
        for pattern, format_type in patterns:
            match = re.search(pattern, text)
            if match:
                try:
                    if format_type == 'DMY':
                        day, month, year = match.groups()
                        date = datetime(int(year), int(month), int(day), 18, 0)
                    elif format_type == 'DMY_SHORT':
                        day, month, year = match.groups()
                        year = int('20' + year) if int(year) < 50 else int('19' + year)
                        date = datetime(year, int(month), int(day), 18, 0)
                    elif format_type == 'YMD':
                        year, month, day = match.groups()
                        date = datetime(int(year), int(month), int(day), 18, 0)
                    
                    # Only return dates in the future
                    if date > datetime.now():
                        return date.isoformat()
                except (ValueError, TypeError):
                    continue
        
        # Default to next week if no valid date found
        return (datetime.now() + timedelta(days=7)).replace(hour=18, minute=0).isoformat()
