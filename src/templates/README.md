# Site Generator Templates

This directory contains template files used by `src/modules/site_generator.py` to generate the static site.

## KISS Templating Approach

We use **simple Python string formatting** (no templating engines like Jinja2):
- Templates are plain HTML/JS files with `{placeholder}` syntax
- Python uses `.format()` method to substitute values
- No external dependencies - pure standard library

## Template Files

- **index.html** - Main HTML structure template
- **config-loader.js** - Runtime configuration loader script
- **fetch-interceptor.js** - Fetch API interceptor for embedded data

## Usage

```python
from pathlib import Path

# Load template
template_path = Path(__file__).parent / 'templates' / 'index.html'
template = template_path.read_text(encoding='utf-8')

# Simple substitution with .format()
html = template.format(
    app_name="My App",
    favicon="data:image/svg+xml,...",
    leaflet_css="/* CSS content */",
    # ... other placeholders
)
```

## Why Not Jinja2 or Other Engines?

Following KISS principles:
- ✅ No external dependencies
- ✅ Simple and readable
- ✅ Fast (no parsing overhead)
- ✅ Easy to debug (plain files)
- ✅ Fits our use case (static generation)

## Editing Templates

1. Edit the template files directly (HTML/JS)
2. Placeholders use `{name}` syntax
3. The generator module reads and substitutes values
4. Run `python3 src/event_manager.py generate` to test
