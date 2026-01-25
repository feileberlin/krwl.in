# Roboto Mono Font - Setup Required

## Status: Font File Needs to Be Fetched

### Option 1: Automatic (Recommended)
```bash
python3 src/event_manager.py dependencies fetch
```

### Option 2: Manual Download

```bash
# Roboto Mono Regular (14 KB)
curl -o roboto-mono-regular-latin.woff2 \
  'https://fonts.gstatic.com/s/robotomono/v23/L0xuDF4xlVMF-BfR8bXMIhJHg45mwgGEFl0_3vq_ROW4.woff2'
```

### After Adding Files

```bash
git add lib/roboto-mono/
git commit -m "Add Roboto Mono font for offline PR previews"
```

## Why This File?

Roboto Mono is used for code blocks and monospace text. Total size: ~14 KB
