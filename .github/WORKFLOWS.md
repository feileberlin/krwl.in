# GitHub Workflows - Complete Reference

## Overview

This project uses a **three-tier workflow architecture** that replaced the previous monolithic `website-maintenance.yml` (1752 lines). Each workflow has a single, focused responsibility.

---

## 📊 Workflow Categorization

### **Tier 1: Core Automation** (Scheduled + Push)
Workflows that run automatically to keep the site operational.

| Workflow | Trigger | Purpose |
|----------|---------|---------|
| [`scheduled-scraping.yml`](#scheduled-scraping) | Scheduled (4 AM, 4 PM Berlin) | Scrape events & weather twice daily |
| [`deploy.yml`](#deploy) | Push to main | Build & deploy to GitHub Pages |
| [`monthly-archive.yml`](#monthly-archive) | 1st of month | Archive old events (retention policy) |

### **Tier 2: Manual Operations** (workflow_dispatch)
Workflows triggered manually via GitHub UI for on-demand operations.

| Workflow | Purpose |
|----------|---------|
| [`manual-scrape.yml`](#manual-scrape) | On-demand event/weather scraping |
| [`editorial-workflow.yml`](#editorial-workflow) | Review & publish pending events |
| [`maintenance.yml`](#maintenance) | Force rebuild, update deps, diagnostics |
| [`telegram-bot-handler.yml`](#telegram-bot-handler) | Process Telegram bot events (repository_dispatch) |

### **Tier 3: CI/CD & Quality** (pull_request + push)
Workflows that validate code quality and provide PR previews.

| Workflow | Trigger | Purpose |
|----------|---------|---------|
| [`ci-tests.yml`](#ci-tests) | PRs & push to main | Linting, tests, config validation |
| [`pr-preview.yml`](#pr-preview) | PRs | Build preview artifacts |
| [`dependency-check.yml`](#dependency-check) | Weekly (Mondays) | Security audit & outdated packages |

### **Utility Workflows** (Not Part of Three-Tier Architecture)
Standalone workflows for specific maintenance tasks.

| Workflow | Category | Purpose |
|----------|----------|---------|
| [`delete-branches.yml`](#delete-branches) | **Utility** | One-time branch cleanup (manual, with confirmation) |

---

## 🔧 Shared Infrastructure

### Composite Actions
- **`.github/actions/setup-python-env/action.yml`**
  - Reusable Python setup (Python 3.x + pip cache + requirements install)
  - Used by all workflows to eliminate duplication

---

## 📖 Detailed Workflow Descriptions

### <a name="scheduled-scraping"></a>`scheduled-scraping.yml`
**Tier 1: Core Automation**

**Triggers:**
- Schedule: `0 3 * * *` (4:00 AM Berlin) - Morning update
- Schedule: `0 15 * * *` (4:00 PM Berlin) - Afternoon update
- Manual: `workflow_dispatch` with `force_scrape` option

**Jobs:**
1. **scrape-events** - Scrapes events from RSS/HTML sources → commits to `pending_events.json`
2. **scrape-weather** - Scrapes weather data → commits to `weather_cache.json` (force-added if gitignored)

**Key Features:**
- Sequential jobs with git pull/rebase to avoid conflicts
- Automatic commit & push to trigger deployment
- Handles gitignored weather cache file

---

### <a name="deploy"></a>`deploy.yml`
**Tier 1: Core Automation**

**Triggers:**
- Push to `main` branch (ALL commits, no path filters)
- Manual: `workflow_dispatch`

**Jobs:**
1. **build** - Fetches dependencies, generates static site, uploads artifact
2. **deploy** - Deploys artifact to GitHub Pages

**Key Features:**
- Single responsibility: get code to production
- Triggered by ALL main branch pushes (prevents silent deployment failures)
- Uses GitHub Pages environment with proper authentication

---

### <a name="monthly-archive"></a>`monthly-archive.yml`
**Tier 1: Core Automation**

**Triggers:**
- Schedule: `0 2 1 * *` (1st of month at 02:00 UTC)
- Manual: `workflow_dispatch` with `dry_run` option

**Jobs:**
1. **archive-events** - Archives events older than retention window (default: 60 days)

**Key Features:**
- Dry-run mode for safety (default: enabled)
- Commits archived events to monthly files
- Keeps active events list performant

---

### <a name="manual-scrape"></a>`manual-scrape.yml`
**Tier 2: Manual Operations**

**Triggers:**
- Manual only: `workflow_dispatch`

**Inputs:**
- `scrape_events` (bool) - Scrape events from sources
- `scrape_weather` (bool) - Scrape weather data
- `force_refresh` (bool) - Bypass cache
- `trigger_deploy` (bool) - Trigger deployment after scraping

**Jobs:**
1. **scrape-events** - On-demand event scraping
2. **scrape-weather** - On-demand weather scraping (with git pull/rebase)
3. **trigger-deployment** - Info message (deploy happens via push)

**Key Features:**
- Flexible options for selective scraping
- Sequential jobs with conflict resolution
- Triggered by actor tracked in commits

---

### <a name="editorial-workflow"></a>`editorial-workflow.yml`
**Tier 2: Manual Operations**

**Triggers:**
- Manual only: `workflow_dispatch`

**Inputs:**
- `action` (choice) - Editorial action: list-pending, publish, reject, bulk-publish, bulk-reject
- `event_ids` (string) - Event ID(s) or pattern (supports wildcards for bulk)
- `auto_deploy` (bool) - Auto-deploy after publishing (default: true)

**Jobs:**
1. **editorial-action** - Executes chosen action via `event_manager.py`

**Key Features:**
- Content curation interface via GitHub UI
- Bulk operations with pattern matching
- Automatic deployment on publish

---

### <a name="maintenance"></a>`maintenance.yml`
**Tier 2: Manual Operations**

**Triggers:**
- Manual only: `workflow_dispatch`

**Inputs:**
- `task` (choice) - Maintenance task: force-rebuild, update-dependencies, validate-config, show-capabilities
- `trigger_deploy` (bool) - Deploy after task

**Jobs:**
1. **maintenance-task** - Executes chosen maintenance task

**Key Features:**
- Force rebuild for troubleshooting
- Dependency updates (Leaflet.js, etc.)
- Config validation
- Scraper diagnostics (capabilities JSON)

---

### <a name="telegram-bot-handler"></a>`telegram-bot-handler.yml`
**Tier 2: Manual Operations**

**Triggers:**
- `repository_dispatch` events:
  - `telegram_flyer_submission` - Flyer OCR processing
  - `telegram_contact_submission` - Contact form messages
  - `telegram_pin_submission` - PIN-based publishing
- Manual: `workflow_dispatch` with `test_mode` option

**Jobs:**
1. **process-telegram-flyer** - Processes flyer submissions (external bot handles OCR locally)
2. **process-telegram-contact** - Creates GitHub issues for contact messages
3. **process-telegram-pin** - Processes PIN publishing (external bot handles validation)

**Key Features:**
- Receives events from external Telegram bot (`telegram_bot_simple.py`)
- Bot runs on external server with `TELEGRAM_BOT_TOKEN` + `GITHUB_TOKEN`
- Acts as fallback/legacy handler (bot handles most processing locally)
- Safe payload handling (uses `toJson` to prevent injection)

**Architecture:**
```
External Server (telegram_bot_simple.py)
  ↓ sends repository_dispatch
GitHub Actions (telegram-bot-handler.yml)
  ↓ creates issues / commits events
Repository (events.json, pending_events.json)
```

---

### <a name="ci-tests"></a>`ci-tests.yml`
**Tier 3: CI/CD & Quality**

**Triggers:**
- Pull requests: opened, synchronize, reopened
- Push to `main` branch

**Path Filters:**
- `src/**`, `tests/**`, `assets/**`, `config.json`, `features.json`, `requirements.txt`

**Jobs:**
1. **validate-config** - Validates `config.json` and `features.json`
2. **lint** - Python syntax check (via `find` + `py_compile`), JSON validation
3. **test** - Runs test suite (feature verification, scraper tests, schema validation, filter tests)
4. **kiss-check** - KISS principle compliance check

**Key Features:**
- Fast feedback for PRs (no deployment)
- Comprehensive validation pipeline
- Minimal permissions (no write access)

---

### <a name="pr-preview"></a>`pr-preview.yml`
**Tier 3: CI/CD & Quality**

**Triggers:**
- Pull requests: opened, synchronize, reopened

**Path Filters:**
- `src/**`, `assets/**`, `config.json`, `.github/workflows/pr-preview.yml`

**Jobs:**
1. **build-preview** - Builds preview site, uploads artifact, comments on PR

**Key Features:**
- Uses PR commit SHA (not branch ref) for deterministic builds
- 7-day artifact retention
- Updates existing PR comment instead of creating duplicates
- No production deployment (preview only)

---

### <a name="dependency-check"></a>`dependency-check.yml`
**Tier 3: CI/CD & Quality**

**Triggers:**
- Schedule: `0 8 * * 1` (Every Monday at 08:00 UTC)
- Manual: `workflow_dispatch`

**Jobs:**
1. **check-dependencies** - Scans for outdated packages, runs pip-audit for vulnerabilities

**Key Features:**
- Creates GitHub issues for:
  - Security vulnerabilities (any count)
  - Outdated packages (>5 packages)
- Weekly security audit
- Automated issue creation with detailed reports

---

### <a name="delete-branches"></a>`delete-branches.yml`
**Utility Workflow** (Not Part of Three-Tier Architecture)

**Category:** Utility / Maintenance

**Triggers:**
- Manual only: `workflow_dispatch`

**Inputs:**
- `dry_run` (bool) - Preview mode (default: true)
- `confirm_deletion` (string) - Must type "DELETE ALL BRANCHES" to confirm

**Jobs:**
1. **delete-branches** - Deletes all branches except `main`

**Key Features:**
- One-time cleanup task (not part of regular automation)
- Safety mechanisms:
  - Dry-run mode by default
  - Explicit confirmation required
  - Preserves `main` branch
- Provides detailed summary of actions

**Why Not in Three-Tier Architecture:**
- Not core automation (doesn't need scheduling)
- Not manual operation (too dangerous for frequent use)
- Not CI/CD (doesn't validate code quality)
- Special-purpose utility for one-time cleanup

---

## 🔄 Workflow Dependencies

```
scheduled-scraping.yml
  ├─> scrape-events (commits)
  └─> scrape-weather (commits, depends on scrape-events)
       ↓ (push to main)
       └─> deploy.yml (triggered by push)
            └─> GitHub Pages (deployed)

manual-scrape.yml
  ├─> scrape-events (commits)
  └─> scrape-weather (commits, depends on scrape-events)
       ↓ (push to main)
       └─> deploy.yml (triggered by push)

editorial-workflow.yml (commits)
  ↓ (push to main)
  └─> deploy.yml (triggered by push)

monthly-archive.yml (commits)
  ↓ (push to main)
  └─> deploy.yml (triggered by push)

PR → ci-tests.yml (validate)
  └─> pr-preview.yml (build artifact)

Weekly → dependency-check.yml (security audit)

External Telegram Bot → telegram-bot-handler.yml
```

---

## 🔐 Permissions Matrix

| Workflow | contents | pages | id-token | issues | pull-requests |
|----------|----------|-------|----------|--------|---------------|
| scheduled-scraping | write | - | - | - | - |
| deploy | read | write | write | - | - |
| monthly-archive | write | - | - | - | - |
| manual-scrape | write | - | - | - | - |
| editorial-workflow | write | - | - | - | - |
| maintenance | write | - | - | - | - |
| telegram-bot-handler | write | - | - | write | - |
| ci-tests | read | - | - | - | - |
| pr-preview | read | - | - | - | write |
| dependency-check | read | - | - | write | - |
| delete-branches | write | - | - | - | - |

**Principle:** Minimal permissions per workflow (least privilege)

---

## 🔒 Concurrency Groups

Each workflow has its own concurrency group to prevent conflicts:

| Workflow | Group | Cancel in progress? |
|----------|-------|---------------------|
| scheduled-scraping | `scheduled-scraping` | ❌ No (let scrapes finish) |
| deploy | `deploy-${{ github.ref }}` | ❌ No (let deploys finish) |
| monthly-archive | `monthly-archive` | ❌ No (let archiving finish) |
| manual-scrape | `manual-scrape` | ✅ Yes (cancel old manual runs) |
| editorial-workflow | `editorial-workflow` | ❌ No (let edits finish) |
| maintenance | `maintenance` | ✅ Yes (cancel old maintenance) |
| telegram-bot-handler | `telegram-bot-${{ github.event.action }}` | ❌ No (process all events) |
| ci-tests | `ci-tests-${{ github.ref }}` | ✅ Yes (cancel outdated CI) |
| pr-preview | `pr-preview-${{ github.event.pull_request.number }}` | ✅ Yes (cancel outdated previews) |
| dependency-check | `dependency-check` | ❌ No (let checks finish) |
| delete-branches | N/A (no concurrency group) | N/A |

---

## 📝 Migration Notes

### From Monolithic Workflow

**Before:** `website-maintenance.yml` (1752 lines)
- Mixed all responsibilities
- Difficult to debug failures
- Slow CI (PRs triggered scraping)
- Single concurrency group for everything

**After:** 10 focused workflows (~550 total lines)
- Single responsibility per workflow
- Easy to debug (smaller scope)
- Fast CI (PRs only run tests)
- Granular concurrency control

**Deprecated Files:**
- `website-maintenance.yml` → `website-maintenance.yml.deprecated`
- `auto-generate-html.yml.deprecated` (removed)
- `config-validation.yml.deprecated` (removed)
- `pr-preview.yml.deprecated` (removed)
- `wishlist-ci.yml.deprecated` (removed)

### Rollback Plan

If issues arise:
1. Restore `website-maintenance.yml` (remove `.deprecated` suffix)
2. Disable new workflows by renaming them
3. Investigate and fix issues
4. Re-attempt migration

---

## 🧪 Testing Strategy

### Tier 1 (Core Automation)
1. Manually trigger `scheduled-scraping.yml` via workflow_dispatch
2. Verify events and weather are scraped and committed
3. Confirm `deploy.yml` triggers on push to main
4. Wait for scheduled runs (4 AM, 4 PM Berlin time)

### Tier 2 (Manual Operations)
1. Test each manual workflow with different input combinations
2. Verify `editorial-workflow.yml` publishes events correctly
3. Test `maintenance.yml` tasks (rebuild, dependencies, etc.)
4. Simulate Telegram events for `telegram-bot-handler.yml`

### Tier 3 (CI/CD)
1. Create test PR to trigger `ci-tests.yml`
2. Verify `pr-preview.yml` builds artifact and comments
3. Wait for `dependency-check.yml` scheduled run (Monday)

### Utility
1. Test `delete-branches.yml` in dry-run mode
2. Verify confirmation mechanism works
3. Test actual deletion on non-production repository

---

## 📚 Additional Resources

- **Copilot Instructions:** `.github/copilot-instructions.md`
- **Feature Registry:** `features.json`
- **Event Manager CLI:** `python3 src/event_manager.py --help`
- **Telegram Integration:** `IMPLEMENTATION_TELEGRAM.md`
- **Original Issue:** Problem statement in PR description

---

## ❓ FAQ

**Q: Why are there 10 workflows instead of 1?**
A: Single responsibility principle. Each workflow has one clear purpose, making it easier to debug, maintain, and optimize.

**Q: Can I trigger multiple workflows at once?**
A: Yes, workflows are independent. You can run manual workflows in parallel.

**Q: What happens if a scheduled workflow fails?**
A: GitHub will retry. Check the Actions tab for logs. Each workflow is isolated, so failures don't cascade.

**Q: How do I add a new workflow?**
A: Determine which tier it belongs to, create the file, test it, and update this documentation.

**Q: Why is `delete-branches.yml` not in the three-tier architecture?**
A: It's a special-purpose utility workflow for one-time cleanup, not part of regular operations.

**Q: How does the Telegram bot integration work?**
A: External bot (`telegram_bot_simple.py`) sends `repository_dispatch` events to `telegram-bot-handler.yml`. The bot handles most processing locally (OCR, PIN validation) and uses GitHub Actions as a fallback.

---

*This documentation is auto-generated. Last updated: 2026-01-25*
