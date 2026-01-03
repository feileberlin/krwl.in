# Changelog

All notable changes to the KRWL HOF Community Events project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## January 2026

### Added

- **PR #69** (2026-01-01): Consolidate data to static/, add individual event backups, simplify workflows
- **PR #73** (2026-01-01): Add bulk operations for event review workflow
- **PR #74** (2026-01-01): Add wildcard pattern support to bulk approve/reject commands
- **PR #75** (2026-01-01): [WIP] Add feature to auto-reject recurring events
- **PR #77** (2026-01-01): [WIP] Implement Facebook Graph API integration for event scraping
- **PR #80** (2026-01-01): feat: add modular SmartScraper system with AI providers, image analysis, and multi-interface configuration
- **PR #85** (2026-01-01): Add scraper options configuration to all event sources
- **PR #88** (2026-01-01): Add CHANGELOG.md with v1.0.0 release history
- **PR #90** (2026-01-01): [WIP] Add demo events display to index.html
- **PR #92** (2026-01-01): [WIP] Add manual library download workflow for GitHub Actions
- **PR #93** (2026-01-02): Add workflow for committing and pushing repository changes
- **PR #99** (2026-01-02): Mark unimplemented deployment features and update verifier to skip them
- **PR #108** (2026-01-02): Add interactive time drawer with dynamic marker scaling for sunrise filter
- **PR #110** (2026-01-02): Add keyboard navigation for map and event browsing
- **PR #113** (2026-01-02): Reconfigure filter sentence: add megaphone logo and simplify structure (KISS)
- **PR #117** (2026-01-02): Populate noscript tags with sorted event data and add automatic SVG inlining
- **PR #118** (2026-01-02): Add simple environment override to config.json, remove .env files
- **PR #119** (2026-01-02): Simplify watermark to single function following KISS principles with i18n support
- **PR #120** (2026-01-02): Add comprehensive linting to HTML export process
- **PR #121** (2026-01-02): Add dual GitHub Actions workflows and KISS templating for automated deployment
- **PR #130** (2026-01-03): Add automated Markdown-to-HTML documentation build system
- **PR #131** (2026-01-03): Update Lucide CDN to use @latest with proper dev/prod URLs

### Changed

- **PR #72** (2026-01-01): [WIP] Update features.json to reference scrape-events.yml
- **PR #76** (2026-01-01): Replace 2185-line generator.py with 324-line CDN inliner (86% reduction)
- **PR #87** (2026-01-01): Organize Python helper scripts into scripts/ and tests/ directories
- **PR #91** (2026-01-01): [WIP] Move location status to watermark infos
- **PR #94** (2026-01-02): Eliminate GitHub Pages artifacts: generate self-contained HTML with unified script
- **PR #102** (2026-01-02): Refactor to platform-agnostic site generator with runtime configuration and setup guide
- **PR #104** (2026-01-02): Remove redundant documentation from .github, update README
- **PR #106** (2026-01-02): Unify config files with automatic multi-platform environment detection
- **PR #107** (2026-01-02): KISS refactor: integrate README generation with GitHub About updates
- **PR #109** (2026-01-02): Consolidate documentation to README.md and switch to ENVIRONMENT variable
- **PR #111** (2026-01-02): [WIP] Update event templates to trigger on reload with relative times
- **PR #112** (2026-01-02): Restore missing watermark HTML element
- **PR #115** (2026-01-02): Show main-content after events load and filter description updates
- **PR #123** (2026-01-02): [WIP] Rename filter bar elements for clarity and consistency
- **PR #127** (2026-01-02): Raise time-drawer z-index above edge details
- **PR #128** (2026-01-03): Switch application to development mode

### Fixed

- **PR #70** (2026-01-01): Fix debug deployment: correct publish paths and add config.debug.json
- **PR #71** (2026-01-01): Rename debug environment to preview for consistency with branch name
- **PR #81** (2026-01-01): [WIP] Fix boolean input in configure-scraper workflow
- **PR #82** (2026-01-01): [WIP] Fix syntax error in Add New Source step
- **PR #83** (2026-01-01): [WIP] Fix NameError in scraper workflow due to boolean input
- **PR #84** (2026-01-01): [WIP] Fix NameError for source_enabled in scraper configuration
- **PR #86** (2026-01-01): Fix misleading "new events found" message when only timestamp updated
- **PR #96** (2026-01-02): Fix JavaScript concatenation syntax error in HTML generator
- **PR #97** (2026-01-02): Fix 404.html redirect logic for nested paths
- **PR #98** (2026-01-02): Add missing GitHub Pages deployment workflows for feature verification
- **PR #103** (2026-01-02): Remove GitHub Actions, consolidate documentation, restructure directories with event-data separation
- **PR #105** (2026-01-02): Fix outdated src/main.py references in copilot-instructions.md
- **PR #114** (2026-01-02): Add app-ready signal for reliable screenshot capture
- **PR #116** (2026-01-02): Clean up HTML structure and enhance watermark with live filter stats
- **PR #126** (2026-01-03): Fix logo path border color to match text and prevent timestamp merge conflicts
- **PR #129** (2026-01-03): Inline Lucide icon markers as base64 with configurable category mapping

### Removed

- **PR #100** (2026-01-02): Clean up obsolete files and reorganize project structure
- **PR #101** (2026-01-02): Reorganize root directory - move files to appropriate subdirectories
- **PR #122** (2026-01-02): Consolidate docs/ folder into README and inline comments per KISS philosophy

---

## December 2025

### Added

- **PR #2** (2025-12-08): [WIP] Add GitHub Actions workflow for static directory deployment
- **PR #4** (2025-12-08): Implement auto-zoom to fit markers, geolocation fallback, and user-selectable filters with natural language description
- **PR #5** (2025-12-09): Add feature registry, KISS compliance monitoring, configurable linting, inline interactive filters, modular Python architecture with CLI/TUI/Daemon modes, configuration editor, and night mode map UI
- **PR #8** (2025-12-09): [WIP] Add test for event examples and JSON event schema comparison
- **PR #13** (2025-12-09): copilot/add-time-filter-options
- **PR #17** (2025-12-29): Replace logo with inline megaphone SVG across all assets
- **PR #25** (2025-12-29): Add Copilot instructions for repository
- **PR #37** (2025-12-29): Add environment watermark with build metadata and GitHub UI deployment integration
- **PR #40** (2025-12-29): Include category filter in map overlay sentence when set to "all"
- **PR #46** (2025-12-30): Implement fullscreen map with pure JavaScript filter dropdowns
- **PR #50** (2025-12-29): Inline events.json data into HTML to eliminate network request

### Changed

- **PR #1** (2025-12-08): Community events system for Hof, Bavaria with geolocation/sunrise filtering, auto-archiving, and contextual UI
- **PR #6** (2025-12-09): Transform event list sidebar to fullscreen terminal-styled map with burger menu actions
- **PR #9** (2025-12-09): [WIP] Optimize text color scheme for better visibility
- **PR #12** (2025-12-09): Move event count from separate selector into category filter text
- **PR #14** (2025-12-28): copilot/count-events-by-category
- **PR #27** (2025-12-29): [WIP] Refactor static changes using generator.py for UI and filters
- **PR #28** (2025-12-29): [WIP] Configure custom instructions and development environment
- **PR #29** (2025-12-29): [WIP] Make unified CLI entry point and update TUI accordingly
- **PR #31** (2025-12-29): [WIP] Update documentation for GitHub Wiki compatibility
- **PR #35** (2025-12-29): [WIP] Update workflow permissions for GitHub Actions
- **PR #44** (2025-12-29): [WIP] Reenable CartoDB Dark No Labels layer
- **PR #45** (2025-12-29): Merge event-count and event-list into interactive filter sentence with mobile-first design
- **PR #52** (2025-12-30): Update watermark to white translucent, reduce logo stroke-width, re-center logo
- **PR #54** (2025-12-30): [WIP] Update leaflet markers to barbie red
- **PR #56** (2025-12-30): Update deprecated GitHub Actions artifact actions from v3 to v4
- **PR #59** (2025-12-30): [WIP] Design project with monochromatic shades of barbie red
- **PR #62** (2025-12-30): [WIP] Update watermark to improve visibility and details
- **PR #64** (2025-12-30): [WIP] Disable borders around watermark and filter sentence

### Fixed

- **PR #3** (2025-12-08): Add two-step deployment workflow with debug mode and demo event generation
- **PR #7** (2025-12-09): Fix documentation builder permissions, add local Leaflet hosting, i18n system, and comprehensive marker library
- **PR #10** (2025-12-09): Fix i18n time labels and category filter, complete PR #9 security scan
- **PR #11** (2025-12-09): Add i18n to popups, fix duplicate filters, implement category-specific icons
- **PR #16** (2025-12-29): Add automated twice-daily event scraping via GitHub Actions with configurable timezone
- **PR #22** (2025-12-29): Fix generator templates to preserve UI changes and prevent overwrites
- **PR #23** (2025-12-29): [WIP] Fix documentation builder failures
- **PR #26** (2025-12-29): [WIP] Fix issue with manual run of GitHub Actions in pages
- **PR #32** (2025-12-29): Document GitHub Wiki initialization requirement
- **PR #34** (2025-12-29): Consolidate documentation to docs/ directory for simplified wiki sync
- **PR #36** (2025-12-29): Fix promote-preview workflow: add validation, auto-branch creation, and v7 upgrade
- **PR #41** (2025-12-29): Implement missing debug mode and multi-data-source features, fix documentation paths
- **PR #48** (2025-12-29): Fix filter dropdowns and implement edge-positioned event details with SVG arrows
- **PR #49** (2025-12-29): Fix map tile loading background color mismatch
- **PR #55** (2025-12-30): Fix YAML parsing errors in workflows with inline Python scripts
- **PR #57** (2025-12-30): Fix feature verification regex patterns for auto-generated static files
- **PR #58** (2025-12-30): Fix JSON decode error in KISS compliance workflow by redirecting warnings to stderr
- **PR #60** (2025-12-30): Fix KISS compliance check workflow failure due to import-time warnings
- **PR #61** (2025-12-30): Fix JSON validation errors: Remove JSONC comments from config files
- **PR #63** (2025-12-30): [WIP] Fix EOF error during static site generation
- **PR #65** (2025-12-30): Fix Leaflet CDN blocking and remove undefined method call

### Removed

- **PR #15** (2025-12-29): Make filter dropdowns mobile-first and remove language switcher
- **PR #39** (2025-12-29): [WIP] Remove div with id events-list
- **PR #47** (2025-12-29): Remove header and event list, reposition logo inline with filter sentence
- **PR #51** (2025-12-30): UI refinements: larger barbie red megaphone logo, removed reload button, enabled production watermark
- **PR #66** (2025-12-30): Align megaphone logo icon with filter text and remove borders

---

## Project Information

### Repository
- **URL**: https://github.com/feileberlin/krwl-hof
- **Issues**: https://github.com/feileberlin/krwl-hof/issues
- **Discussions**: https://github.com/feileberlin/krwl-hof/discussions

### Contributing
For information on how to contribute, see the [README.md](README.md) file.

---

*Last Updated: 2026-01-03*
*This file is auto-generated from Git history. Do not edit manually.*
