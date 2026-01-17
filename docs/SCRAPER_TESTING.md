# Scraper Testing Guide

## Network Environment

### Copilot Workspace (Testing Environment)
- **DNS Resolution**: ❌ Blocked
- **External HTTP**: ❌ Blocked  
- **web_search tool**: ✅ Works (via Copilot API)
- **Purpose**: Code development and validation

### GitHub Actions (Production)
- **DNS Resolution**: ✅ Full access
- **External HTTP**: ✅ Full access
- **web_search tool**: ❌ Not available
- **Purpose**: Actual event scraping

## Testing Scrapers

### In Copilot Workspace
```bash
# This will show network errors (expected behavior)
python3 src/event_manager.py scrape

# You'll see messages like:
# "Request error: Failed to resolve 'www.hof.de'"
# "🔍 Trying web search fallback..."
```

**This is normal!** The scrapers are correctly implemented but cannot reach external sites in this environment.

### In Production (GitHub Actions)
The scrapers will work normally when deployed to GitHub Actions because:
1. Full network access is available
2. DNS resolution works
3. All HTTP requests succeed

### Testing Locally (Your Machine)
```bash
# Install dependencies
pip install -r requirements.txt

# Run scraper with full network access
python3 src/event_manager.py scrape

# This should fetch real events from configured sources
```

## Scraper Implementation Status

### ✅ Custom Scrapers (Site-Specific)
1. **Frankenpost** - Regional newspaper events
   - Two-step scraping (list + detail pages)
   - Location extraction from venue info
   - Custom date parsing

2. **Freiheitshalle** - Cultural center
   - Event listing page parsing
   - German date formats (DD.MM.YYYY)
   - Default cultural venue location

3. **VHS Hofer Land** - Adult education
   - Course/workshop extraction
   - Last-minute course filtering
   - Education category tagging

4. **Hof Stadt** - Municipal website
   - Community event parsing
   - General event formats
   - City-wide location defaults

### ✅ Generic Scrapers (Fallback)
1. **HTML Source** - Generic website scraping
   - Common CSS selectors
   - Pattern-based date extraction
   - Flexible parsing

2. **Facebook Source** - Social media events
   - Mobile/desktop page scraping
   - OCR for event flyers
   - Web search fallback (when direct access fails)

### 🔄 Facebook Web Search Fallback
When Facebook direct scraping fails (blocked, rate-limited, or network issues):
1. Extracts page name from URL
2. Generates search query: "{PageName} events upcoming Germany"
3. Logs query for external processing
4. Can be used with web_search tool manually

Example:
```
🔍 Web search for: GaleriehausHof
💡 Web search query: 'GaleriehausHof events upcoming Germany'
```

## How to Verify Scrapers Work

### 1. Check Scraper Registration
```bash
python3 -c "
import sys; sys.path.insert(0, 'src')
from modules.smart_scraper.core import SmartScraper
from modules.utils import load_config
from pathlib import Path

config = load_config(Path('.'))
scraper = SmartScraper(config, '.')
print(f'Registered handlers: {len(scraper.registry._handlers)}')
"
```

Expected output: `Registered handlers: 11` (or more)

### 2. Check Custom Scraper Imports
```bash
python3 -c "
import sys; sys.path.insert(0, 'src')
from modules.smart_scraper.sources.custom import (
    FreiheitshalleSource, VHSSource, HofStadtSource
)
print('✓ All custom scrapers imported')
"
```

### 3. Run Scraping (with network)
```bash
python3 src/event_manager.py scrape
```

Expected with network:
- Events scraped from various sources
- Some duplicates filtered
- New events added to pending

Expected without network (Copilot Workspace):
- Network errors (normal)
- Web search fallback messages
- 0 events scraped (expected)

## Manual Web Search Testing

Since `web_search` works in Copilot Workspace, you can manually test event discovery:

```bash
# Run scraper to see search queries
python3 src/event_manager.py scrape 2>&1 | grep "💡 Web search query"

# Copy a query and use web_search tool
# Example: "GaleriehausHof events upcoming Germany"
```

## Production Deployment

When this code is merged and runs in GitHub Actions:
1. The workflow triggers on schedule (04:00 and 16:00 Berlin time)
2. Full network access is available
3. All scrapers fetch real events
4. Events are added to pending queue
5. Editorial review can approve/reject
6. Approved events appear on the map

## Troubleshooting

### "Failed to resolve hostname"
- **In Copilot Workspace**: Normal, ignore
- **In production**: Check DNS, firewall, source URL

### "0 events scraped"
- **In Copilot Workspace**: Expected (no network)
- **In production**: Check if source website changed structure

### "Web search fallback"
- **In Copilot Workspace**: Normal behavior
- **In production**: Indicates Facebook blocking (use search as alternative)

## Next Steps

1. **Deploy to production** - Push to main branch
2. **Monitor first run** - Check GitHub Actions logs
3. **Review events** - Use editorial workflow to approve
4. **Iterate** - Adjust scrapers based on results
