# Copilot Instructions for KRWL HOF Community Events

## Project Overview

KRWL HOF is a **mobile-first Progressive Web App (PWA)** for discovering community events with interactive map visualization. The project uses a Python backend for event scraping/management and a vanilla JavaScript frontend with Leaflet.js for mapping.

### Architecture
- **Backend**: Python 3.x with modular TUI (Text User Interface)
- **Frontend**: Vanilla JavaScript (no frameworks), Leaflet.js for maps
- **Deployment**: Static site generation (configurable output path via `config.[prod,dev].json` → future `build` section, defaults to `static/index.html`) → Deployed to hosting platform (GitHub Pages, Netlify, Vercel, etc.)
- **Data Flow**: Scraping → Pending queue → Editorial review → Published events

## Technology Stack

### Backend (Python)
- **Core**: Python 3.x, modular design
- **Dependencies**: requests>=2.31.0, beautifulsoup4>=4.12.0, lxml>=4.9.0, feedparser>=6.0.10 (see `requirements.txt`)
- **Key Modules**:
  - `src/event_manager.py` - ⭐ CLI entry point, TUI, and event management (SINGLE SOURCE OF TRUTH)
  - `src/modules/scraper.py` - Event scraping (RSS, HTML, API)
  - `src/modules/editor.py` - Editorial workflow
  - `src/modules/site_generator.py` - HTML generation and build system
  - `src/modules/filter_tester.py` - Filter testing
  - `src/modules/feature_verifier.py` - Feature registry validation

### Frontend (JavaScript)
- **Framework**: None (vanilla JS)
- **Maps**: Leaflet.js
- **PWA**: Manifest.json for installability (service worker planned for future)
- **i18n**: Custom implementation (`static/js/i18n.js`)
- **Files**: 
  - `static/index.html` - Main app
  - `static/js/app.js` - App logic
  - `static/css/style.css` - Styles

### Configuration
- `config.prod.json` - Production (optimized, real events only)
- `config.dev.json` - Development (debug enabled, demo events, DEV badge)

## ⚠️ CRITICAL: Single Entry Point

**There is ONLY ONE entry point: `src/event_manager.py`**

- ❌ **`src/main.py` does NOT exist** (and should never be created)
- ✅ **`src/event_manager.py`** contains:
  - CLI argument parsing (`main()` function)
  - TUI (Text User Interface) implementation (`EventManagerTUI` class)
  - All CLI commands (scrape, publish, reject, generate, etc.)

**If you see references to `src/main.py` anywhere:**
- They are **outdated** and should be replaced with `src/event_manager.py`
- Update documentation, scripts, and instructions accordingly

**Usage:**
```bash
# Launch TUI
python3 src/event_manager.py

# CLI commands
python3 src/event_manager.py scrape
python3 src/event_manager.py generate
python3 src/event_manager.py --help
```

## 📁 Project Structure

### Complete Directory Tree

```
krwl-hof/
│
├── .github/
│   ├── workflows/           # CI/CD automation
│   └── copilot-instructions.md  # This file
│
├── src/
│   ├── event_manager.py     # ⭐ SINGLE ENTRY POINT - CLI & TUI
│   └── modules/
│       ├── scraper.py       # Event scraping logic
│       ├── editor.py        # Editorial workflow
│       ├── site_generator.py # HTML generation & build system
│       ├── utils.py         # Common utilities
│       ├── config_editor.py # Config management TUI
│       ├── workflow_launcher.py # GitHub Actions launcher
│       ├── filter_tester.py # Filter testing
│       ├── feature_verifier.py # Feature registry validation
│       ├── kiss_checker.py  # KISS principle validator
│       └── scheduler.py     # Scheduling utilities
│
├── static/
│   ├── index.html          # 🚫 AUTO-GENERATED (do not edit directly)
│   ├── events.json         # Published events data
│   ├── pending_events.json # Events awaiting approval
│   ├── rejected_events.json # Rejected events log
│   ├── content.json        # English translations
│   ├── content.de.json     # German translations
│   ├── manifest.json       # PWA manifest
│   ├── css/
│   │   └── style.css       # ✅ Edit this for styles
│   └── js/
│       ├── app.js          # ✅ Edit this for app logic
│       └── i18n.js         # ✅ Edit this for i18n logic
│
├── tests/
│   ├── test_scraper.py
│   ├── test_filters.py
│   ├── test_event_schema.py
│   ├── test_translations.py
│   └── ... (other test files)
│
├── config.prod.json        # Production configuration
├── config.dev.json         # Development configuration
├── features.json           # Feature registry (MUST update when adding features)
└── requirements.txt        # Python dependencies
```

### Module Purposes & When to Edit

| Module | Purpose | Edit When... |
|--------|---------|--------------|
| `src/event_manager.py` | CLI entry point & TUI | Adding CLI commands, TUI menus, or main workflow |
| `src/modules/scraper.py` | Event scraping | Adding/modifying scraping logic or sources |
| `src/modules/editor.py` | Editorial workflow | Changing approval/rejection flow |
| `src/modules/site_generator.py` | HTML generation | Modifying build process or HTML templates |
| `src/modules/utils.py` | Common utilities | Adding shared helper functions |
| `src/modules/config_editor.py` | Config management | Changing config TUI or validation |
| `src/modules/workflow_launcher.py` | GitHub Actions | Modifying CI/CD integration |
| `static/js/app.js` | Frontend logic | Adding map features, filters, or UI behavior |
| `static/css/style.css` | Styles | Changing appearance, layout, or themes |
| `static/js/i18n.js` | Internationalization | Modifying translation loading or fallback |
| `config.[prod,dev].json` | Configuration | Adding settings, sources, or options |
| `features.json` | Feature registry | **ALWAYS** when adding new features |

### Frontend File Edit Policy

✅ **DO edit these source files:**
- `static/css/style.css`
- `static/js/app.js`
- `static/js/i18n.js`
- `static/content.json` / `static/content.de.json`

🚫 **DO NOT edit generated files:**
- `static/index.html` (regenerated by `site_generator.py`)

After editing source files, regenerate with:
```bash
python3 src/event_manager.py build production  # or development
```

## 🗺️ Decision Tree: Where to Place New Code

```
┌─ Is this a new feature? ─────────────────────┐
│                                               │
│  ┌─ YES → Update features.json FIRST         │
│  │         (otherwise tests will fail!)      │
│  │                                            │
│  └─ What type of feature?                    │
│       │                                       │
│       ├─ Data/Events related?                │
│       │   ├─ Scraping → src/modules/scraper.py
│       │   ├─ Editorial → src/modules/editor.py
│       │   └─ Management → src/event_manager.py
│       │                                       │
│       ├─ UI/Frontend related?                │
│       │   ├─ Styling → static/css/style.css │
│       │   ├─ Logic → static/js/app.js       │
│       │   └─ i18n → static/js/i18n.js       │
│       │             + content.[en|de].json   │
│       │                                       │
│       ├─ Build/Generation related?           │
│       │   └─ src/modules/site_generator.py   │
│       │                                       │
│       ├─ Configuration related?              │
│       │   ├─ Settings → config.[prod,dev].json
│       │   └─ Config UI → src/modules/config_editor.py
│       │                                       │
│       ├─ Workflow/CI related?                │
│       │   ├─ GitHub Actions → .github/workflows/
│       │   └─ Launcher → src/modules/workflow_launcher.py
│       │                                       │
│       └─ Utility/Helper related?             │
│           └─ src/modules/utils.py            │
│                                               │
└───────────────────────────────────────────────┘
```

### Rules for New Code Placement

1. **Never create top-level Python files** - All Python code belongs in `src/` or `src/modules/`
2. **Never create `src/main.py`** - Use `src/event_manager.py` only
3. **Backend changes go in `src/modules/`** - Keep event_manager.py focused on CLI/TUI
4. **Frontend changes go in `static/`** - Edit CSS/JS source files, never `index.html`
5. **Always update `features.json`** - Required for all new features

## 🚫 Anti-Patterns: What NOT to Do

### ❌ DON'T: Create duplicate entry points
```python
# ❌ BAD: Creating src/main.py
# src/main.py
if __name__ == "__main__":
    # This duplicates event_manager.py functionality
```

### ✅ DO: Use the single entry point
```python
# ✅ GOOD: Use src/event_manager.py
python3 src/event_manager.py scrape
```

---

### ❌ DON'T: Edit auto-generated files
```html
<!-- ❌ BAD: Editing static/index.html directly -->
<style>
  .new-style { color: red; }
</style>
```

### ✅ DO: Edit source files and regenerate
```css
/* ✅ GOOD: Edit static/css/style.css */
.new-style { color: red; }
```
```bash
python3 src/event_manager.py build production
```

---

### ❌ DON'T: Create top-level Python files
```
krwl-hof/
├── my_new_script.py  # ❌ BAD: Top-level script
```

### ✅ DO: Add to appropriate module
```
krwl-hof/
├── src/
│   └── modules/
│       └── my_new_module.py  # ✅ GOOD: In modules/
```

---

### ❌ DON'T: Skip feature registry updates
```python
# ❌ BAD: Adding feature without updating features.json
# Feature verification tests will fail!
```

### ✅ DO: Always update features.json
```json
// ✅ GOOD: Add entry to features.json
{
  "id": "my-new-feature",
  "name": "My New Feature",
  "description": "What it does",
  "category": "backend",
  "implementation_files": ["src/modules/my_new_module.py"]
}
```

---

### ❌ DON'T: Mix backend and frontend code
```python
# ❌ BAD: HTML generation in scraper.py
def scrape_events():
    events = get_events()
    return f"<html>{events}</html>"  # Wrong layer!
```

### ✅ DO: Keep layers separated
```python
# ✅ GOOD: Scraper returns data only
def scrape_events():
    return get_events()  # Data layer

# site_generator.py handles HTML generation
```

---

### ❌ DON'T: Hardcode configuration
```python
# ❌ BAD: Hardcoded values
MAX_DISTANCE = 5.0
DEFAULT_LAT = 50.3167
```

### ✅ DO: Use config files
```python
# ✅ GOOD: Load from config
config = load_config()
MAX_DISTANCE = config['filtering']['max_distance_km']
DEFAULT_LAT = config['map']['default_center']['lat']
```

## ✅ Quick Reference Checklists

### Pre-Implementation Checklist

Before writing code:
- [ ] Read through the Critical Single Entry Point section
- [ ] Identify which module(s) need changes using the Decision Tree
- [ ] Check if similar functionality already exists (avoid duplication)
- [ ] Plan where to add tests (in `tests/` directory)
- [ ] Review KISS principles in `src/modules/kiss_checker.py`

### Implementation Checklist

While coding:
- [ ] Edit source files only (never auto-generated files)
- [ ] Add/update tests in `tests/` directory
- [ ] Follow existing code style and patterns
- [ ] Keep changes minimal and focused
- [ ] Add docstrings for complex functions
- [ ] Use `src/event_manager.py` for all CLI commands

### Post-Implementation Checklist

After coding:
- [ ] Update `features.json` if adding new features
- [ ] Run relevant tests: `python3 tests/test_*.py --verbose`
- [ ] Verify KISS compliance: `python3 src/modules/kiss_checker.py`
- [ ] Run feature verification: `python3 src/modules/feature_verifier.py --verbose`
- [ ] If frontend changes: `python3 src/event_manager.py build production`
- [ ] Test manually (run TUI, check generated HTML, etc.)
- [ ] Update documentation if needed

### Pull Request Requirements

Before submitting PR:
- [ ] All tests pass
- [ ] No references to `src/main.py` exist
- [ ] `features.json` is up to date
- [ ] Auto-generated files are committed if changed
- [ ] KISS principles followed
- [ ] Code review requested if significant changes


## Critical: Auto-Generated Files 🚫

**DO NOT manually edit this file** - it is generated by `src/modules/site_generator.py`:
- `static/index.html` - Single-file HTML with everything inlined

### To modify the HTML:
1. Edit source CSS/JS files: `static/css/style.css`, `static/js/app.js`, `static/js/i18n.js`
2. Or edit templates in `src/modules/site_generator.py` (for advanced changes)
3. Run: `python3 src/event_manager.py build production` (or `development`)
4. Commit both source changes AND generated `static/index.html`

## Build and Test Instructions

### Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Download frontend libraries (Leaflet.js)
python3 src/event_manager.py libs

# Verify library integrity
python3 src/event_manager.py libs verify
```

### Running Locally
```bash
# Start local server
cd static
python3 -m http.server 8000
# Open http://localhost:8000
```

### Testing (ALWAYS run before finalizing changes)

#### Quick Development Tests
```bash
# Feature verification (validates features.json registry)
python3 verify_features.py --verbose

# Scraper tests
python3 test_scraper.py --verbose

# Filter tests
python3 test_filters.py --verbose

# Event schema validation
python3 test_event_schema.py --verbose

# KISS principle compliance
python3 check_kiss.py --verbose

# Translation tests
python3 test_translations.py --verbose

# Scheduler tests
python3 test_scheduler.py --verbose
```

#### Documentation
```bash
# Regenerate README.md (auto-generated)
python3 scripts/generate_readme.py
```

#### Linting
- **Python**: Linting is advisory (warnings don't block PRs)
- **JavaScript**: ESLint for syntax checking
- **JSON**: Strict validation (blocks PRs on errors)

See `.github/workflows/lint.yml` for full linting configuration.

### Building the Application
```bash
# Build production HTML (optimized, real events only)
python3 src/event_manager.py build production

# Build development HTML (with demo events and DEV badge)
python3 src/event_manager.py build development

# Fast event update (after scraping or publishing, no full rebuild)
python3 src/event_manager.py events

# Legacy command (still works, uses site_generator)
python3 src/event_manager.py generate
```

## Code Guidelines

### KISS Principle (Keep It Simple, Stupid)
This project follows **strict KISS principles**. Always:
- Minimize complexity
- Avoid over-engineering
- Use vanilla solutions over frameworks when possible
- Keep files small and focused
- Avoid unnecessary abstractions

**Enforcement**: `check_kiss.py` validates KISS compliance. Review `src/modules/kiss_checker.py` for rules.

### Python Style
- **Python 3.x** standard library preferred
- **Type hints**: Not required but appreciated
- **Docstrings**: Use for modules and complex functions
- **Error handling**: Comprehensive try/except blocks
- **Module structure**: Keep modules under 1000 lines

### JavaScript Style
- **ES6+** features are okay (async/await, arrow functions, etc.)
- **No frameworks**: Vanilla JS only (Leaflet.js is the only external library)
- **Progressive Enhancement**: App must work without JavaScript for basic content
- **Mobile First**: Always test on mobile viewport sizes

### CSS Style
- **Mobile First**: Write for mobile, enhance for desktop
- **CSS Variables**: Use for theming (see `static/css/style.css`)
- **Responsive**: Use media queries, flexbox, grid
- **Accessibility**: Ensure sufficient contrast, focus indicators

## Feature Registry System

All features must be documented in `features.json` with:
- Unique ID
- Name and description
- Category: `backend`, `frontend`, or `infrastructure`
- Implementation files
- Config keys (if applicable)
- Test method

**Validation**: Run `python3 verify_features.py` to ensure registry matches codebase.

When adding features:
1. Implement the feature
2. Add entry to `features.json`
3. Run `python3 verify_features.py --verbose` to validate

## Testing Requirements

### For Backend Changes
- Add/update tests in `test_*.py` files
- Run relevant test suite before committing
- Ensure tests pass in CI/CD

### For Frontend Changes
- Test in Chrome, Firefox, Safari
- Test on mobile devices (or Chrome DevTools mobile emulation)
- Verify PWA functionality (installability, offline mode)
- Check accessibility (keyboard navigation, screen readers)

### For Configuration Changes
- Test with both `config.dev.json` and `config.prod.json`
- Validate JSON syntax
- Run full test suite

## Deployment Workflow

Simplified workflow with two modes:

1. **Feature branch** → PR to `main` branch
2. **Main branch** → Auto-deploys to production (uses `config.prod.json`)

GitHub Pages serves the `static/` directory directly.

### Build Modes:
- **Production**: Real events only, optimized
- **Development**: Real + demo events, DEV badge shown

## Documentation Standards

### README.md
**AUTO-GENERATED** by `scripts/generate_readme.py`. Do not edit directly.
- Run `python3 scripts/generate_readme.py` to regenerate

### Code Documentation
- Python modules: Docstring at top of file
- Complex functions: Docstring explaining purpose, args, returns
- Configuration: Comments in JSON files (where parser allows)

### Markdown Files
- Use ATX-style headers (`#`, `##`, etc.)
- Include code blocks with language specifiers
- Add examples where helpful
- Keep lines under 120 characters when possible

## Workflow-Specific Guidelines

### Event Scraping
1. Configure source in `config.json` under `scraping.sources[]`
2. Implement scraper logic in `src/modules/scraper.py` if needed
3. Test with: `python3 test_scraper.py --verbose`
4. Scraped events go to `static/pending_events.json` for editorial review

### Editorial Workflow
1. Pending events require approval (unless `editor.auto_publish: true`)
2. Use TUI: `python3 src/event_manager.py` → "Review Pending Events"
3. Or use GitHub UI: Actions → "Review Events (GitHub UI)" → Run workflow
4. Actions: approve (a), edit (e), reject (r)
5. Approved events → `static/events.json` → appear on map
6. Approved events backed up to `backups/events/`

### Static Generation
1. HTML is generated by `src/modules/site_generator.py`
2. Generate: `python3 src/event_manager.py build production` (or `development`)
3. Fast event update: `python3 src/event_manager.py events` (no full rebuild)
4. Output: `static/index.html` (single-file HTML with everything inlined)
5. Data files live directly in `static/` (events.json, config files, etc.)

## Security Considerations

- **No secrets in code**: Use environment variables or config files (gitignored)
- **Input validation**: Always sanitize user input and scraped data
- **XSS protection**: Escape HTML when displaying user-generated content
- **HTTPS**: Production must use HTTPS (enforced by GitHub Pages)

## Common Tasks

### Add a new event source
1. Edit `config.prod.json` (production) or `config.dev.json` (development) in root directory
2. Add to `scraping.sources[]` array
3. Specify `type` (rss, html, api) and `url`
4. Test: `python3 src/event_manager.py scrape`

### Build the application
1. For production: `python3 src/event_manager.py build production`
2. For development: `python3 src/event_manager.py build development`
3. Fast event update: `python3 src/event_manager.py events`

### Add a new filter
1. Edit `static/js/app.js` (filter logic)
2. Edit `static/css/style.css` (filter UI styles)
3. Rebuild: `python3 src/event_manager.py build production`
4. Test: `python3 test_filters.py --verbose`

### Add a new translation
1. Edit `static/content.json` (English)
2. Edit `static/content.de.json` (German)
3. Use in code: `i18n.t('key.path')`
4. Test: `python3 test_translations.py --verbose`

### Update documentation
1. Run: `python3 scripts/generate_readme.py` to regenerate README.md
2. Commit generated `README.md`

## Accessibility (A11y)

- **WCAG 2.1 Level AA** compliance required
- **Keyboard navigation**: All interactive elements must be keyboard accessible
- **ARIA labels**: Use for dynamic content and complex widgets
- **Color contrast**: Minimum 4.5:1 for normal text, 3:1 for large text
- **Focus indicators**: Visible focus styles required
- **Screen readers**: Test with NVDA (Windows) or VoiceOver (Mac/iOS)

## Performance

- **Page load**: Target < 3 seconds
- **Time to Interactive**: Target < 5 seconds
- **First Contentful Paint**: Target < 1.5 seconds
- **JavaScript bundle**: Keep minimal (vanilla JS helps)
- **Images**: Optimize, use SVG where possible
- **Caching**: Production uses aggressive caching via `config.prod.json`

## Git Workflow

### Commit Messages
- Use conventional commits: `feat:`, `fix:`, `docs:`, `test:`, `refactor:`, etc.
- Keep first line under 72 characters
- Add body for complex changes

### Branch Naming
- Feature: `feature/description`
- Fix: `fix/description`
- Copilot: `copilot/description` (auto-generated by Copilot)

### Pull Requests
- Target `main` branch
- Provide clear description
- Link related issues
- Ensure CI passes

## Questions or Issues?

- Check `README.md` for comprehensive guide
- Check `features.json` for feature registry documentation
- Run CLI commands with `--help` for detailed usage information

## Remember

1. **Test before committing** - Run relevant test suite
2. **Don't edit auto-generated files** - Edit source CSS/JS files instead
3. **Follow KISS principles** - Keep it simple
4. **Document features** - Update `features.json`
5. **Validate schemas** - Run `python3 test_event_schema.py`
6. **Check accessibility** - Test keyboard navigation and screen readers

## CLI Commands Reference

All commands are run through `src/event_manager.py`:

### Build Commands
- `python3 src/event_manager.py build production` - Build HTML (production mode)
- `python3 src/event_manager.py build development` - Build HTML (development mode with demo events)
- `python3 src/event_manager.py events` - Fast event update (no full rebuild)
- `python3 src/event_manager.py libs` - Download CDN libraries
- `python3 src/event_manager.py libs verify` - Verify libraries are installed

### Event Management
- `python3 src/event_manager.py scrape` - Scrape events from sources
- `python3 src/event_manager.py list` - List published events
- `python3 src/event_manager.py list-pending` - List pending events
- `python3 src/event_manager.py publish EVENT_ID` - Approve a pending event
- `python3 src/event_manager.py reject EVENT_ID` - Reject a pending event
- `python3 src/event_manager.py bulk-publish "pending_*"` - Bulk approve (supports wildcards)
- `python3 src/event_manager.py bulk-reject "pending_*"` - Bulk reject (supports wildcards)

### Utility
- `python3 src/event_manager.py` - Interactive TUI
- `python3 src/event_manager.py --help` - Show all commands
- `python3 src/event_manager.py generate` - Legacy command (uses site_generator)
