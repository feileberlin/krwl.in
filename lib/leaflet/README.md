# Leaflet Dependencies - Setup Required

## Status: Dependencies Need to Be Fetched

The Leaflet library files are not yet in this directory. To add them:

### Option 1: Automatic (Recommended)
```bash
python3 src/event_manager.py dependencies fetch
```

### Option 2: Manual Download

Download these files from https://unpkg.com/leaflet@1.9.4/dist/:

1. **leaflet.css** (14 KB)
   ```bash
   curl -o leaflet.css https://unpkg.com/leaflet@1.9.4/dist/leaflet.css
   ```

2. **leaflet.js** (150 KB)
   ```bash
   curl -o leaflet.js https://unpkg.com/leaflet@1.9.4/dist/leaflet.js
   ```

3. **Marker images** (create images/ subdirectory)
   ```bash
   mkdir -p images
   cd images
   curl -LO https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png
   curl -LO https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon-2x.png
   curl -LO https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png
   ```

### After Adding Files

Once files are downloaded, commit them:

```bash
git add lib/leaflet/
git commit -m "Add Leaflet v1.9.4 for offline PR previews"
```

## Why These Files?

These files are committed to the repository to ensure:
- ✅ PR previews work without internet
- ✅ Reviewers see working maps immediately
- ✅ No "Map Loading..." fallback screen

See [../README.md](../README.md) for full explanation.
