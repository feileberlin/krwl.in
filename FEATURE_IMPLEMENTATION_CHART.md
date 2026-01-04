# KRWL HOF Feature Implementation Chart

**Generated**: 2026-01-04

This document maps all features across CLI, TUI, and CI/CD implementations.

---

## 📊 Quick Stats

| Interface | Features/Commands | Description |
|-----------|-------------------|-------------|
| **CLI** | 23 commands | Direct command-line interface via `python3 src/event_manager.py <command>` |
| **TUI** | 8 menu options | Interactive terminal UI (run without arguments) |
| **CI/CD** | 10 jobs | Automated workflows in `website-maintenance.yml` |

---

## 🖥️ CLI Commands

All commands are accessed via: `python3 src/event_manager.py <command>`

### Event Management
1. `scrape` - Scrape new events from configured sources
2. `list` - List all published events
3. `list-pending` - List events awaiting approval
4. `publish <id>` - Approve and publish a pending event
5. `reject <id>` - Reject a pending event
6. `review` - Interactive review of pending events
7. `bulk-publish <pattern>` - Bulk approve events matching pattern
8. `bulk-reject <pattern>` - Bulk reject events matching pattern

### Data Management
9. `clear-data` - Clear all event data (with backup)
10. `load-examples` - Load example/demo events
11. `update` - Update events data without full rebuild

### Archiving
12. `archive` - Archive old events manually
13. `archive-monthly` - Archive events by month
14. `archive-info` - Show archive statistics

### Site Generation
15. `generate` - Generate static site HTML
16. `fetch` - Fetch CDN dependencies (Leaflet, Lucide)

### Development Tools
17. `docs <task>` - Documentation tasks (build, validate, etc.)
18. `test <suite>` - Run test suites
19. `utils <utility>` - Run utility scripts
20. `check` - Run all verification checks
21. `scraper-info` - Show scraper configuration
22. `setup` - Interactive setup wizard
23. `dependencies` - Check/install dependencies

---

## 🎨 TUI Menu Options

Launch with: `python3 src/event_manager.py` (no arguments)

Interactive terminal interface with menu:

1. **Scrape New Events** - Fetch events from configured sources
2. **Review Pending Events** - Approve/reject/edit pending events
3. **View Published Events** - Browse published events
4. **Generate Static Site** - Build HTML for deployment
5. **View Documentation** - Browse project documentation
6. **Settings** - Configure scraper sources and options
7. **📘 Setup Guide** - First-time setup wizard
8. **Exit** - Quit TUI

---

## 🤖 CI/CD Jobs (website-maintenance.yml)

Automated workflow jobs in `.github/workflows/website-maintenance.yml`:

### Discovery & Info
1. `discover-capabilities` - Detect scraper capabilities and config
2. `show-info` - Display configuration and enabled sources
3. `schedule` - Calculate next scheduled run

### Core Operations
4. `scrape-events` - Scrape events (scheduled or manual)
5. `review-pending` - Automated or manual review process
6. `update-events` - Update events.json without full rebuild
7. `full-rebuild` - Complete site regeneration

### Archiving & Deployment
8. `archive-monthly` - Archive old events by month
9. `deploy` - Deploy to GitHub Pages
10. `push` - Commit and push changes

---

## 🗺️ Feature Coverage Matrix

Backend features and their implementation across interfaces:

| Feature | CLI | TUI | CI | Notes |
|---------|-----|-----|----|----|
| **Event Scraping** | ✓ | ✓ | ✓ | Core functionality |
| **Event Review/Edit** | ✓ | ✓ | ✓ | Editorial workflow |
| **Bulk Operations** | ✓ | — | — | CLI-only for safety |
| **Site Generation** | ✓ | ✓ | ✓ | HTML build |
| **Event Archiving** | ✓ | — | ✓ | Monthly archiving |
| **Documentation** | ✓ | ✓ | — | Docs generation/viewing |
| **Testing** | ✓ | — | — | Development only |
| **Setup Wizard** | ✓ | ✓ | — | First-time setup |
| **Dependency Management** | ✓ | — | ✓ | CDN libraries |
| **Configuration** | ✓ | ✓ | — | Scraper config |

---

## 🔄 Workflow Migration

**Previous**: Multiple separate workflow files
- ❌ `archive-monthly.yml` - DELETED (moved to unified workflow)
- ❌ `deploy.yml` - DELETED (moved to unified workflow)
- ❌ `scrape-events.yml` - DELETED (moved to unified workflow)
- ❌ `update-events-data.yml` - DELETED (moved to unified workflow)

**Current**: Single unified workflow
- ✅ `website-maintenance.yml` - ALL-IN-ONE adaptive workflow

**Benefits**:
- Single source of truth
- Automatic capability detection
- No duplicate configuration
- Easier maintenance
- Follows KISS principles

---

## 📝 Usage Examples

### CLI Usage

```bash
# Scrape events and review
python3 src/event_manager.py scrape
python3 src/event_manager.py review

# Bulk approve demo events
python3 src/event_manager.py bulk-publish "demo_*"

# Archive and generate site
python3 src/event_manager.py archive-monthly
python3 src/event_manager.py generate

# Run tests
python3 src/event_manager.py test all
```

### TUI Usage

```bash
# Launch interactive mode
python3 src/event_manager.py

# Then use menu:
# 1 → Scrape events
# 2 → Review pending
# 3 → Generate site
```

### CI/CD Trigger

```bash
# Manually trigger workflow
gh workflow run website-maintenance.yml

# With specific job
gh workflow run website-maintenance.yml -f mode=scrape
```

---

## 🎯 Design Philosophy

### KISS Principle
- **Single entry point**: `src/event_manager.py` for all operations
- **Single workflow**: `website-maintenance.yml` for all automation
- **Consistent interface**: Same functionality accessible via CLI, TUI, or CI

### Modularity
- Core logic in `src/modules/` (reusable)
- CLI/TUI in `src/event_manager.py` (interface)
- CI configuration in `.github/workflows/` (automation)

### No Duplication
- Workflows moved to event_manager modules
- One source of truth for commands
- Configuration drives automation

---

**Last Updated**: 2026-01-04
**Maintained by**: KRWL HOF Team
