# Roboto Fonts - Setup Required

## Status: Font Files Need to Be Fetched

The Roboto font files are not yet in this directory. To add them:

### Option 1: Automatic (Recommended)
```bash
python3 src/event_manager.py dependencies fetch
```

### Option 2: Manual Download

Download these files from Google Fonts:

```bash
# Roboto Regular (13 KB)
curl -o roboto-regular-latin.woff2 \
  'https://fonts.gstatic.com/s/roboto/v30/KFOmCnqEu92Fr1Mu4mxK.woff2'

# Roboto Medium (13 KB)
curl -o roboto-medium-latin.woff2 \
  'https://fonts.gstatic.com/s/roboto/v30/KFOlCnqEu92Fr1MmEU9fBBc4.woff2'

# Roboto Bold (13 KB)
curl -o roboto-bold-latin.woff2 \
  'https://fonts.gstatic.com/s/roboto/v30/KFOlCnqEu92Fr1MmWUlfBBc4.woff2'
```

### After Adding Files

```bash
git add lib/roboto/
git commit -m "Add Roboto fonts for offline PR previews"
```

## Why These Files?

Roboto is the main body font used throughout the app. Committing these fonts ensures:
- ✅ Consistent typography in PR previews
- ✅ No font loading delays
- ✅ Works offline after download

Total size: ~39 KB
