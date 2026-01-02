# Screenshot Generation Guide

## Overview

The KRWL HOF Community Events app now includes a **ready signal** that indicates when the page is fully loaded and ready for screenshot capture. This solves the problem of screenshots being taken before the map and event data have finished loading.

## The Problem

The app performs several asynchronous operations on load:
1. Loading configuration from `config.json`
2. Initializing the Leaflet map
3. Fetching user geolocation
4. Loading event data
5. Rendering markers on the map

Taking screenshots immediately after page load would capture an incomplete state, missing the map tiles, event markers, or other dynamic content.

## The Solution

The app now emits a **ready signal** when all initialization is complete:

### 1. Body Attribute
When ready, the app sets:
```html
<body data-app-ready="true">
```

### 2. Custom Event
The app dispatches a custom event on the `window` object:
```javascript
window.dispatchEvent(new CustomEvent('app-ready', {
    detail: {
        timestamp: Date.now(),
        eventsLoaded: 27,
        mapInitialized: true
    }
}));
```

## Using the Ready Signal

### Playwright (Python)

```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    
    # Set viewport for desired screenshot size
    page.set_viewport_size({"width": 1280, "height": 800})  # Desktop
    # or
    page.set_viewport_size({"width": 390, "height": 844})   # Mobile (iPhone 14)
    
    # Navigate to the page
    page.goto('http://localhost:8000')
    
    # Wait for app to be ready (max 30 seconds)
    page.wait_for_selector('body[data-app-ready="true"]', timeout=30000)
    
    # Optional: Wait a bit more for map tiles to fully render
    page.wait_for_timeout(2000)
    
    # Take screenshot
    page.screenshot(path='screenshot.png', full_page=True)
    
    browser.close()
```

### Puppeteer (Node.js)

```javascript
const puppeteer = require('puppeteer');

(async () => {
  const browser = await puppeteer.launch();
  const page = await browser.newPage();
  
  // Set viewport
  await page.setViewport({ width: 1280, height: 800 });
  
  // Navigate
  await page.goto('http://localhost:8000', { 
    waitUntil: 'networkidle0' 
  });
  
  // Wait for app to be ready
  await page.waitForSelector('body[data-app-ready="true"]', {
    timeout: 30000
  });
  
  // Optional: Additional wait for map tiles
  await page.waitForTimeout(2000);
  
  // Take screenshot
  await page.screenshot({ 
    path: 'screenshot.png',
    fullPage: true
  });
  
  await browser.close();
})();
```

### Selenium (Python)

```python
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Setup driver
driver = webdriver.Chrome()
driver.set_window_size(1280, 800)

# Navigate
driver.get('http://localhost:8000')

# Wait for app to be ready (max 30 seconds)
WebDriverWait(driver, 30).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, 'body[data-app-ready="true"]'))
)

# Optional: Additional wait for map tiles
time.sleep(2)

# Take screenshot
driver.save_screenshot('screenshot.png')
driver.quit()
```

### JavaScript (Browser Console)

```javascript
// Listen for app-ready event
window.addEventListener('app-ready', (event) => {
    console.log('App is ready!', event.detail);
    console.log(`Loaded ${event.detail.eventsLoaded} events`);
    console.log(`Map initialized: ${event.detail.mapInitialized}`);
});

// Or check if already ready
if (document.body.getAttribute('data-app-ready') === 'true') {
    console.log('App is already ready!');
}
```

## Recommended Screenshot Sizes

For PWA manifest compliance:

### Mobile (Narrow Form Factor)
- Width: 640px
- Height: 1136px
- Output: `screenshot-mobile.png`

### Desktop (Wide Form Factor)
- Width: 1280px
- Height: 800px
- Output: `screenshot-desktop.png`

## Complete Example Script

Here's a complete Python script using Playwright to generate both mobile and desktop screenshots:

```python
#!/usr/bin/env python3
"""Generate PWA screenshots for manifest.json"""

from playwright.sync_api import sync_playwright
import sys

def generate_screenshots(url='http://localhost:8000', output_dir='assets'):
    """Generate mobile and desktop screenshots"""
    
    with sync_playwright() as p:
        browser = p.chromium.launch()
        
        # Mobile screenshot
        print("📱 Generating mobile screenshot...")
        page_mobile = browser.new_page()
        page_mobile.set_viewport_size({"width": 640, "height": 1136})
        page_mobile.goto(url)
        page_mobile.wait_for_selector('body[data-app-ready="true"]', timeout=30000)
        page_mobile.wait_for_timeout(2000)  # Wait for map tiles
        page_mobile.screenshot(path=f'{output_dir}/screenshot-mobile.png')
        page_mobile.close()
        print(f"✅ Mobile screenshot saved to {output_dir}/screenshot-mobile.png")
        
        # Desktop screenshot
        print("🖥️  Generating desktop screenshot...")
        page_desktop = browser.new_page()
        page_desktop.set_viewport_size({"width": 1280, "height": 800})
        page_desktop.goto(url)
        page_desktop.wait_for_selector('body[data-app-ready="true"]', timeout=30000)
        page_desktop.wait_for_timeout(2000)  # Wait for map tiles
        page_desktop.screenshot(path=f'{output_dir}/screenshot-desktop.png')
        page_desktop.close()
        print(f"✅ Desktop screenshot saved to {output_dir}/screenshot-desktop.png")
        
        browser.close()
        print("\n✅ All screenshots generated successfully!")

if __name__ == '__main__':
    try:
        generate_screenshots()
    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        sys.exit(1)
```

## Troubleshooting

### Screenshots are still incomplete

1. **Increase timeout**: The default 30-second timeout should be sufficient, but you can increase it if needed.

2. **Add extra wait for map tiles**: Map tiles load asynchronously after the app is ready. Add a 2-3 second wait after the ready signal:
   ```python
   page.wait_for_timeout(2000)  # 2 seconds
   ```

3. **Check network conditions**: Slow network can delay map tile loading. Consider:
   - Using `waitUntil: 'networkidle0'` in Puppeteer
   - Checking browser console for errors

4. **Verify Leaflet loaded**: Check that the Leaflet library is present:
   ```javascript
   console.log(typeof L !== 'undefined' ? '✅ Leaflet loaded' : '❌ Leaflet missing');
   ```

### Event detail is empty

If `event.detail.eventsLoaded` is 0, check:
- Event data files exist (`events.json` or configured sources)
- Network requests succeed (check browser console)
- Config `data.source` setting is correct

## Technical Details

### Implementation Location
- **File**: `assets/js/app.js` (source) → `static/js/app.js` (built)
- **Method**: `EventsApp.markAppAsReady()`
- **Called from**: `EventsApp.init()` after all async operations complete

### Signal Timing
The ready signal is emitted after:
1. ✅ Config loaded
2. ✅ Map initialized
3. ✅ Geolocation requested (or skipped)
4. ✅ Events loaded and processed
5. ✅ Event listeners set up

Note: Map tiles may still be loading after the ready signal. Add a small delay (1-2s) for visual completeness.

## See Also
- [PWA Manifest Documentation](../assets/manifest.json)
- [Event Manager CLI](../README.md#cli-usage)
- [Static Site Generation](../src/modules/site_generator.py)
