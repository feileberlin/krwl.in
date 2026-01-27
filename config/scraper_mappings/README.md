# Scraper Mappings Directory

This directory contains scraper configuration files created via the **Drag'n'Drop Scraper Setup Tool**.

## How It Works

1. **Create Configuration**: Use the Scraper Setup Tool in the dashboard to analyze an event source URL
2. **Drag & Drop Mapping**: Drag data snippets from the analyzed page to schema field drop zones
3. **Export**: Download the generated `*_ci_config.json` file
4. **Add to Repo**: Place the file in this directory (`config/scraper_mappings/`)
5. **Commit & Push**: GitHub Actions will automatically validate and integrate the new scraper

## File Format

Each configuration file follows this structure:

```json
{
  "version": "2.0",
  "source": {
    "name": "source_name",
    "url": "https://example.com/events",
    "type": "html",
    "enabled": true
  },
  "container": {
    "selector": ".event"
  },
  "field_mappings": {
    "title": {
      "selector": ".event-title",
      "extraction": "text",
      "required": true
    },
    "location_name": {
      "selector": ".venue",
      "extraction": "text",
      "required": true
    },
    "start_date": {
      "selector": ".date",
      "extraction": "datetime",
      "required": true
    }
  },
  "metadata": {
    "created_at": "2025-01-27T19:00:00Z",
    "created_by": "scraper-setup-tool-web"
  }
}
```

## Required Fields

The following fields **must** be mapped for a scraper configuration to be valid:

- `title` - Event title/name
- `location_name` - Venue/location name  
- `start_date` - Start date/time

## GitHub Actions Integration

When a new `*_ci_config.json` file is added:

1. **Validation Job**: Checks JSON structure and required fields
2. **Test Job**: Analyzes the URL to verify selectors work
3. **Integration Job**: Adds the source to `config.json` (main branch only)

See `.github/workflows/scraper-setup.yml` for the full workflow.

## Manual Testing

Test a configuration locally:

```bash
# Analyze URL
python3 src/modules/scraper_setup_api.py --analyze "https://example.com/events"

# List saved configurations
python3 src/modules/scraper_setup_api.py --list
```

## Troubleshooting

- **Selector not finding elements**: Use browser DevTools to verify CSS selectors
- **Date parsing issues**: Check the date format and adjust extraction method
- **Page requires JavaScript**: Static scraping may not work; consider using dynamic scrapers
