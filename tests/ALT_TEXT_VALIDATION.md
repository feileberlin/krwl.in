# Alt Text Quality Validation

This directory contains **dual-layer validation** for alt text quality:

## 1. Build-Time Validation (Regex-Based)

**File:** `src/modules/linter.py`  
**Function:** `lint_accessibility()`

### What It Checks:
- ✅ Alt attributes exist (WCAG 1.1.1)
- ✅ **NEW:** Generic alt text patterns
  - `alt="marker"` → ⚠️ Warning
  - `alt="icon"` → ⚠️ Warning  
  - `alt="image"` → ⚠️ Warning
  - `alt="music event marker"` → ⚠️ Warning (category-only, missing event title)

### Limitations:
- Cannot validate JavaScript template variable values (`${category}`)
- Cannot check context or semantic meaning beyond patterns
- Runs during build, catches issues early

### Usage:
```bash
python3 src/event_manager.py generate
# Automatically runs linter and reports warnings
```

---

## 2. Runtime Validation (HTML Parsing)

**File:** `tests/test_alt_text_quality.py`  
**Type:** Python test script

### What It Checks:
- ✅ Alt text format correctness
- ✅ Event markers include title + category
- ✅ Location markers use popup text
- ✅ No generic patterns in **rendered** HTML
- ✅ Quality of actual alt text values (not just existence)

### Advantages:
- Validates **actual rendered values** in generated HTML
- Catches issues regex can't detect
- Verifies JavaScript template output
- Can detect subtle quality issues

### Usage:
```bash
# Generate HTML first
python3 src/event_manager.py generate

# Run runtime validation
python3 tests/test_alt_text_quality.py
```

### Example Output:
```
======================================================================
ALT TEXT QUALITY VALIDATION SUITE
======================================================================

✓ Event Marker Format: PASS
✓ Location Marker Format: PASS  
✓ Alt Text Quality: PASS

🎉 ALL TESTS PASSED - Alt text is descriptive and accessible!
```

---

## Dual-Layer Strategy

| Layer | Type | When | Catches |
|-------|------|------|---------|
| **Build-Time** | Regex patterns | During `generate` | Generic patterns, common mistakes |
| **Runtime** | HTML parsing | After `generate` | Actual rendered values, template output |

### Why Both?

1. **Build-Time (Linter):**
   - Fast feedback during development
   - Catches obvious mistakes early
   - Integrated into CI/CD pipeline

2. **Runtime (Test):**
   - Validates actual output
   - Catches template variable issues
   - Comprehensive quality checks
   - Can be part of test suite

---

## Example: What Each Layer Catches

### Scenario: Generic Alt Text

**Bad Code:**
```javascript
html: `<img src="${iconUrl}" alt="${category} event marker" />`
```

**Build-Time Linter:**
- ❌ Can't detect this is bad (template variable)
- ✅ But if HTML contains `alt="music event marker"`, warns about generic pattern

**Runtime Test:**
- ✅ Parses generated HTML
- ✅ Sees `alt="music event marker"`
- ✅ Flags as generic (missing event title)

### Scenario: Good Alt Text

**Good Code:**
```javascript
const eventTitle = event.title ? event.title.substring(0, 30) : 'Event';
const altText = `${eventTitle} - ${category} marker`;
html: `<img src="${iconUrl}" alt="${altText}" />`
```

**Build-Time Linter:**
- ✅ No generic pattern warnings in static code

**Runtime Test:**
- ✅ Validates format includes both title and category
- ✅ Confirms rendered output: `alt="Jazz Concert - music marker"`
- ✅ Passes all quality checks

---

## Adding New Checks

### To Build-Time Linter:
Edit `src/modules/linter.py`, add pattern to `generic_alt_patterns`:
```python
generic_alt_patterns = [
    # ...existing patterns...
    (r'alt\s*=\s*["\']your-pattern["\']', "Your warning message"),
]
```

### To Runtime Test:
Edit `tests/test_alt_text_quality.py`, add check to `check_generic_alt_text()`:
```python
generic_patterns = [
    # ...existing patterns...
    (r'^your-pattern$', "Your reason"),
]
```

---

## CI Integration

Both layers can run in CI:

```yaml
- name: Generate site
  run: python3 src/event_manager.py generate
  
- name: Run runtime validation
  run: python3 tests/test_alt_text_quality.py
```

Build-time warnings appear in build logs.  
Runtime test fails CI if quality issues found.

---

## References

- **WCAG 1.1.1:** Non-text Content  
- **WCAG 2.4.4:** Link Purpose (In Context)  
- **Build-Time Code:** `src/modules/linter.py` (line 433-462)
- **Runtime Code:** `tests/test_alt_text_quality.py`
