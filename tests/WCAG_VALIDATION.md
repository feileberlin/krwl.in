# WCAG Accessibility Validation with Performance Timing

This directory contains **dual-layer validation** for WCAG 2.1 Level AA compliance with performance timing to measure validation speed.

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
- ✅ Lang attribute on html tag (WCAG 3.1.1)
- ✅ Links have text content (WCAG 2.4.4)
- ✅ Form inputs have labels (WCAG 3.3.2)
- ✅ Heading hierarchy (WCAG 1.3.1)
- ✅ Skip navigation links (WCAG 2.4.1)

### Performance:
- **Timing displayed:** Shows execution time after each check
- **Typical time:** <0.1s for full HTML validation

### Limitations:
- Cannot validate JavaScript template variable values (`${category}`)
- Cannot check context or semantic meaning beyond patterns
- Runs during build, catches issues early

### Usage:
```bash
python3 src/event_manager.py generate
# Automatically runs linter and reports warnings
# Output: ⏱️  Accessibility check completed in 0.052s
```

---

## 2. Runtime Validation (HTML Parsing)

**File:** `tests/test_accessibility_runtime.py`  
**Type:** Python test script

### What It Checks:
- ✅ Alt text format correctness
- ✅ Event markers include title + category
- ✅ Location markers use popup text
- ✅ No generic patterns in **rendered** HTML
- ✅ Quality of actual alt text values (not just existence)

### Performance:
- **Individual test timing:** Each test shows its own execution time
- **Overall timing:** Total runtime validation time displayed
- **Typical time:** <0.1s for all checks

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
python3 tests/test_accessibility_runtime.py
```

### Example Output:
```
======================================================================
WCAG ACCESSIBILITY RUNTIME VALIDATION SUITE
======================================================================

✓ Event Marker Format: PASS
⏱️  Event marker format check completed in 0.003s

✓ Location Marker Format: PASS  
⏱️  Location marker format check completed in 0.002s

✓ Alt Text Quality: PASS
⏱️  Alt text validation completed in 0.045s

======================================================================
FINAL RESULTS:
======================================================================
Event Marker Format:    ✅ PASS
Location Marker Format: ✅ PASS
Alt Text Quality:       ✅ PASS

⏱️  Total runtime validation time: 0.050s

🎉 ALL TESTS PASSED - WCAG accessibility standards met!
```

---

## Dual-Layer Strategy with Performance Monitoring

| Layer | Type | When | Catches | Typical Time |
|-------|------|------|---------|--------------|
| **Build-Time** | Regex patterns | During `generate` | Generic patterns, common mistakes | <0.1s |
| **Runtime** | HTML parsing | After `generate` | Actual rendered values, template output | <0.1s |

### Why Both?

1. **Build-Time (Linter):**
   - Fast feedback during development (<0.1s)
   - Catches obvious mistakes early
   - Integrated into CI/CD pipeline
   - **Performance tracked:** Shows timing for optimization

2. **Runtime (Test):**
   - Validates actual output (<0.1s)
   - Catches template variable issues
   - Comprehensive quality checks
   - Can be part of test suite
   - **Performance tracked:** Individual and total timing

### Performance Benefits:

- **Fast validation:** Both layers complete in <0.2s total
- **No bottleneck:** Accessibility checks don't slow down builds
- **Optimization ready:** Timing data helps identify slow checks
- **CI-friendly:** Quick enough for every commit

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
- ⏱️  Completes in ~0.05s

**Runtime Test:**
- ✅ Parses generated HTML
- ✅ Sees `alt="music event marker"`
- ✅ Flags as generic (missing event title)
- ⏱️  Completes in ~0.05s

### Scenario: Good Alt Text

**Good Code:**
```javascript
const eventTitle = event.title ? event.title.substring(0, 30) : 'Event';
const altText = `${eventTitle} - ${category} marker`;
html: `<img src="${iconUrl}" alt="${altText}" />`
```

**Build-Time Linter:**
- ✅ No generic pattern warnings in static code
- ⏱️  Completes in ~0.05s

**Runtime Test:**
- ✅ Validates format includes both title and category
- ✅ Confirms rendered output: `alt="Jazz Concert - music marker"`
- ✅ Passes all quality checks
- ⏱️  Completes in ~0.05s

---

## Performance Optimization

### Monitoring:
- **Build-time:** `⏱️  Accessibility check completed in X.XXXs`
- **Runtime:** `⏱️  Total runtime validation time: X.XXXs`

### Benchmarks:
- Accessibility linting: <0.1s (typical: 0.05s)
- Runtime validation: <0.1s (typical: 0.05s)
- Combined: <0.2s (typical: 0.1s)

### If validation is slow:
1. Check HTML file size (should be <1MB)
2. Reduce regex complexity in linter
3. Optimize HTML parsing in runtime test
4. Consider caching parsed results

---

## CI Integration

Both layers can run in CI with performance tracking:

```yaml
- name: Generate site
  run: python3 src/event_manager.py generate
  # Outputs: ⏱️  Accessibility check completed in X.XXXs
  
- name: Run runtime validation  
  run: python3 tests/test_accessibility_runtime.py
  # Outputs: ⏱️  Total runtime validation time: X.XXXs
```

Build-time warnings appear in build logs.  
Runtime test fails CI if quality issues found.
Performance timing helps identify bottlenecks.

---

## References

- **WCAG 1.1.1:** Non-text Content  
- **WCAG 2.4.4:** Link Purpose (In Context)
- **WCAG 3.1.1:** Language of Page
- **WCAG 3.3.2:** Labels or Instructions
- **Build-Time Code:** `src/modules/linter.py` (line 417-540)
- **Runtime Code:** `tests/test_accessibility_runtime.py`
