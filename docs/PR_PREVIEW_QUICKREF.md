# PR Preview Quick Reference Card

> One-page reference for the KISS PR preview system

## 🎯 What Is It?

Automatic preview generation for Pull Requests using GitHub Actions artifacts.
- No external services (Netlify, Vercel)
- No configuration needed
- Download & test locally

---

## 📦 What You Get

Every PR automatically generates:

| Item | Description | Location |
|------|-------------|----------|
| **Site Preview** | Full site in development mode | `public/index.html` |
| **Color Preview** | All 23 CSS variables with swatches | `public/color-preview.html` |
| **Screenshots** | Desktop (1920x1080) + Mobile (375x667) | `public/screenshots/` |
| **Build Info** | Metadata and instructions | `PREVIEW_INFO.txt` |

**Download:** Artifacts available for 90 days

---

## 🚀 How to Test a PR (Reviewer)

### Quick Method (30 seconds)
```bash
1. Click download link in PR comment
2. Extract ZIP
3. Open public/index.html in browser
```

### Full Method (Better)
```bash
# After extracting artifact
cd public
python3 -m http.server 8000
# Open http://localhost:8000
```

### View Colors
```bash
# After extracting
open public/color-preview.html  # macOS
xdg-open public/color-preview.html  # Linux
```

---

## 🎛️ How to Disable (Admin)

### Temporary Disable (Recommended)
```
Settings → Actions → Variables → New variable
Name: PR_PREVIEWS_ENABLED
Value: false
```

### Re-enable
```
Delete PR_PREVIEWS_ENABLED variable
OR change value to: true
```

### Alternative: Disable Workflow
```
Actions → PR Preview Build (KISS) → ⋯ → Disable workflow
```

**Full Guide:** [PR_PREVIEW_DISABLE.md](./PR_PREVIEW_DISABLE.md)

---

## 📊 What Gets Generated

### Artifacts
1. **`pr-{number}-preview`** (~3 MB)
   - Full site (development mode)
   - Color preview HTML
   - Screenshots
   - Build metadata

2. **`pr-{number}-screenshots`** (~500 KB)
   - desktop.png
   - mobile.png

### PR Comment
- Download links
- Color variables table (collapsible)
- Screenshot info
- Testing instructions

---

## 🎨 Color Preview Features

**23 CSS Variables Extracted:**
- Primary colors (2)
- Tints (2) - Lighter
- Shades (2) - Darker  
- Tones (2) - Muted
- Backgrounds (3)
- Text colors (3)
- Borders (2)
- Accents (7)

**Formats:**
- HTML with visual swatches
- Markdown table in PR comment
- Categorized display

---

## 📸 Screenshot Features

**Desktop Screenshot:**
- Resolution: 1920x1080
- Full page capture
- Map fully loaded

**Mobile Screenshot:**
- Resolution: 375x667 (iPhone SE)
- Full page capture
- Map fully loaded

**Tool:** Playwright (Chromium)

---

## ⚡ Performance

**Build Time:** ~3-5 minutes
- Site generation: ~2 min
- Screenshots: ~2 min  
- Color preview: ~30 sec
- Upload: ~30 sec

**Actions Minutes:** ~6-7 per PR

**Artifact Size:**
- Main preview: ~2-3 MB
- Screenshots: ~500 KB

---

## 🔍 Status Check

### Is It Enabled?
```bash
# Method 1: Check Actions tab
Actions → PR Preview Build (KISS) → Should see runs

# Method 2: Check variables
Settings → Actions → Variables → Look for PR_PREVIEWS_ENABLED

# Method 3: Open a test PR
Should see workflow run + comment
```

### Is It Working?
```bash
# Check workflow logs
Actions → PR Preview Build (KISS) → Latest run → Logs

# Look for these steps:
✅ Generate preview site
✅ Generate CSS color preview
✅ Install Playwright
✅ Take screenshots
✅ Upload artifacts
✅ Comment on PR
```

---

## 🐛 Troubleshooting

### No Workflow Running
- Check if disabled via `PR_PREVIEWS_ENABLED`
- Check workflow file exists: `.github/workflows/pr-preview.yml`
- Check PR changes relevant paths (CSS, JS, config, etc.)

### No Artifacts
- Wait for workflow to complete (~5 min)
- Check workflow logs for errors
- Verify upload step succeeded

### No PR Comment
- Check workflow permissions (needs `pull-requests: write`)
- Check github-script action succeeded
- Comment may be collapsed - expand all comments

### Screenshots Missing
- Check if Playwright installation succeeded
- Check if local server started
- Look for "Take screenshots" step in logs

### Colors Not Showing
- Check if design-tokens.css exists
- Check if generate_color_preview.py succeeded
- Verify markdown output generated

---

## 📚 Full Documentation

| Guide | Purpose |
|-------|---------|
| [PR_PREVIEW.md](./PR_PREVIEW.md) | Complete usage guide |
| [PR_PREVIEW_DISABLE.md](./PR_PREVIEW_DISABLE.md) | How to disable |
| [PR_PREVIEW_COMPARISON.md](./PR_PREVIEW_COMPARISON.md) | Why artifacts? |
| [PR_PREVIEW_DIAGRAM.md](./PR_PREVIEW_DIAGRAM.md) | Visual workflows |

---

## 💡 Tips & Tricks

### For PR Authors
- Previews generate automatically - no action needed
- Check Actions tab if build fails
- Preview includes demo events (pink markers)

### For Reviewers
- Use local server method for full features
- Check console (F12) for errors
- Test mobile view (resize browser)
- Compare desktop vs mobile screenshots

### For Admins
- Disable during high PR volume to save Actions minutes
- Screenshots add ~2 min per preview (optional)
- Color preview is quick (~30 sec)
- Each PR costs ~6-7 Actions minutes

---

## 🔄 Common Workflows

### Regular PR Review
```
1. PR opened
2. Wait 5 min for preview
3. Download artifact
4. Extract & test
5. Leave review
```

### Disable for Maintenance
```
1. Settings → Variables
2. Add PR_PREVIEWS_ENABLED=false
3. Existing PRs will skip preview
4. Delete variable when done
```

### Quick Color Check
```
1. Download artifact
2. Open color-preview.html
3. Verify color changes
4. No need to test full site
```

### Screenshot-Only Review
```
1. Download pr-{number}-screenshots
2. Check desktop.png and mobile.png
3. Quick visual verification
4. Skip full artifact if no code testing needed
```

---

## ⚙️ Configuration

### Workflow Trigger Paths
Preview only runs when these change:
- `assets/css/**`
- `assets/js/**`
- `assets/html/**`
- `assets/json/**`
- `config.json`
- `src/**`
- `.github/workflows/pr-preview.yml`

### Disable Methods
1. Repository variable (recommended)
2. Workflow dispatch input (testing)
3. Disable workflow (nuclear)

### Environment Detection
- PR previews: Development mode
- Main branch: Production mode
- Automatic detection (no manual toggle)

---

## 🎯 KISS Principles

✅ **Simple:** Just download and test  
✅ **No Setup:** Works out of the box  
✅ **No External Services:** Pure GitHub  
✅ **No Secrets:** Uses GITHUB_TOKEN  
✅ **No Maintenance:** Auto-cleanup  
✅ **Self-Contained:** Artifacts include everything  
✅ **Reversible:** Easy to disable/enable  

---

## 📞 Support

**Need Help?**
- Check workflow logs in Actions tab
- Review [documentation](./PR_PREVIEW.md)
- Open an issue with workflow URL

**Found a Bug?**
- Check if known issue in workflow logs
- Report with: PR number, workflow run URL, error message

---

## 📈 Metrics

**Since Implementation:**
- Total previews generated: Check Actions history
- Success rate: Should be >95%
- Average build time: ~5 minutes
- Artifact downloads: Check artifact list

---

**Quick Links:**
- [Usage Guide](./PR_PREVIEW.md)
- [Disable Guide](./PR_PREVIEW_DISABLE.md)
- [Comparison](./PR_PREVIEW_COMPARISON.md)
- [Diagrams](./PR_PREVIEW_DIAGRAM.md)

**The KISS way to preview PRs!** 🎯
