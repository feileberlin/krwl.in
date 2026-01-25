# Frontend Dependencies

## Overview

This directory contains frontend dependencies (Leaflet.js, fonts) that are **committed to the repository** to ensure PR previews work reliably without requiring internet access.

## Why Commit Dependencies?

**Problem**: PR preview artifacts need working maps for reviewers, but:
- CI environments may block external CDN requests
- Reviewers downloading artifacts may not have internet
- CDN fallbacks require network access to view previews

**Solution**: Commit minimal essential dependencies
- ✅ PR previews work offline after download
- ✅ No "Map Loading..." fallback for reviewers
- ✅ Consistent preview experience across environments

## What's Included

### Required (Committed)
- `lib/leaflet/` - Leaflet.js v1.9.4 (map library)
  - `leaflet.css` (~14 KB)
  - `leaflet.js` (~150 KB)
  - `images/marker-*.png` (marker icons)
- `lib/roboto/` - Roboto font (body text)
  - `roboto-regular-latin.woff2` (~13 KB)
  - `roboto-medium-latin.woff2` (~13 KB)
  - `roboto-bold-latin.woff2` (~13 KB)
- `lib/roboto-mono/` - Roboto Mono font (code/monospace)
  - `roboto-mono-regular-latin.woff2` (~14 KB)

### Generated (Not Committed)
- `lib/lucide/` - Icon library (generated from codebase usage)

## Setup Instructions

### For New Contributors

If the lib/ directories are empty, fetch dependencies:

```bash
# Fetch all dependencies
python3 src/event_manager.py dependencies fetch

# Or manually download
cd lib/leaflet
curl -LO https://unpkg.com/leaflet@1.9.4/dist/leaflet.css
curl -LO https://unpkg.com/leaflet@1.9.4/dist/leaflet.js
mkdir -p images && cd images
curl -LO https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png
curl -LO https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon-2x.png
curl -LO https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png
```

### For Maintainers

To update dependencies:

```bash
# Check current status
python3 src/event_manager.py dependencies check

# Fetch latest versions
python3 src/event_manager.py dependencies fetch

# Commit updated files
git add lib/leaflet lib/roboto lib/roboto-mono
git commit -m "Update frontend dependencies to latest versions"
```

## Trade-offs

### Pros ✅
- PR previews work offline
- No external network dependencies for viewing
- Consistent experience for all reviewers
- Fast page loads (no CDN latency)

### Cons ❌
- ~220 KB added to repository
- Need manual updates for new Leaflet versions
- Goes against "don't commit binaries" principle

**Decision**: The improved preview experience outweighs the repository size cost.

## KISS Compliance

While committing dependencies adds files to git, it follows KISS by:
- ✅ Simple solution (files just work)
- ✅ No complex CDN fallback logic needed
- ✅ Predictable behavior in all environments
- ✅ Fewer moving parts for reviewers

## Alternatives Considered

1. **CDN fallbacks only** ❌
   - Requires internet for previews
   - "Map Loading..." frustration for reviewers
   
2. **GitHub Actions cache** ❌
   - Doesn't persist across forks
   - Still requires internet during build
   
3. **Submodules** ❌
   - Added complexity
   - Still needs internet to initialize
   
4. **Commit dependencies** ✅
   - Simple, reliable, works everywhere

## File Sizes

```
lib/
├── leaflet/         ~180 KB
│   ├── leaflet.css   14 KB
│   ├── leaflet.js   150 KB
│   └── images/       16 KB
├── roboto/           39 KB
│   ├── regular      13 KB
│   ├── medium       13 KB
│   └── bold         13 KB
└── roboto-mono/      14 KB
    └── regular      14 KB

Total: ~233 KB
```

## License Information

- **Leaflet**: BSD 2-Clause License
- **Roboto**: Apache License 2.0
- **Roboto Mono**: Apache License 2.0

All dependencies are open-source and license-compatible.

## Updating Dependencies

When Leaflet releases a new version:

1. Update version number in `src/modules/site_generator.py`
2. Run `python3 src/event_manager.py dependencies fetch`
3. Test that maps still work
4. Commit updated files
5. Update this README with new version number

## Questions?

See [docs/PR_PREVIEW.md](../../docs/PR_PREVIEW.md) for more information about PR previews and the dependency system.
