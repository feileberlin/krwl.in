# Multilanguage (i18n) Best Practices for KRWL>

## Overview

This document outlines best practices for maintaining the German/English/Czech multilanguage implementation in KRWL>. Last updated: February 2026

## Current Implementation Status

### ✅ What's Working Well

1. **Complete Translation Coverage**
   - All 85 translation keys present in German (de.json), English (en.json), and Czech (cs.json)
   - No missing keys detected across languages
   - Consistent JSON structure across all translation files

2. **Robust Language Detection**
   - URL-based detection: `/en`, `/de/hof`, etc.
   - LocalStorage persistence: `krwl_language` key
   - Browser language fallback: `navigator.language`
   - Config-based default: `config.defaultLanguage = "de"`

3. **Proper Fallback Chain**
   - Translation missing → English fallback
   - Load failure → English cascade
   - Console warnings for debugging
   - Returns key itself if all else fails

4. **URL Routing Architecture**
   - Single language: `/en` → English + default region
   - Language + region: `/de/hof` → German + Hof region
   - Region only: `/hof` → default language + Hof (backward compatible)
   - Root path: `/` → Browser detect or config default

5. **Variable Interpolation**
   - Consistent `{{variable}}` syntax across all languages
   - Works correctly with template strings
   - Example: `"not without a {{dresscode}}"` → `"nicht ohne {{dresscode}}"`

### ⚠️ Areas for Improvement

1. **Region-Specific Language Override Not Implemented**
   - **Issue**: Config defines `regions.*.defaultLanguage` but code doesn't use it
   - **Impact**: Visiting `/hof` defaults to global `config.defaultLanguage` (de) instead of region preference
   - **Example**: `regions.antarctica.defaultLanguage = "en"` is ignored
   - **Recommendation**: Implement region-specific language detection in `app.js` `applyRegionFromUrl()`

2. **English Phrasing Could Be More Natural**
   - **Current**: `"til Sunday's primetime"`
   - **Better**: `"until Sunday at primetime"` or `"until Sunday evening"`
   - **Note**: German "bis Sonntag zur besten Sendezeit" is correct and idiomatic

3. **No Language Negotiation Beyond English**
   - **Issue**: Missing translation → English fallback only
   - **Could improve**: Try region-specific language or browser language first
   - **Example**: Czech user with missing key → English, not German (even if German region)

## Translation Quality Guidelines

### 1. Article Usage (German vs English)

**German requires proper gender articles:**
- ❌ Bad: `"Benutzerprofil"` (missing article)
- ✅ Good: `"das Benutzerprofil"`

**English often omits articles where German requires them:**
- EN: `"user profile"` (no article)
- DE: `"das Benutzerprofil"` (article required)

**Context matters for article omission:**
```json
{
  "en": "not without a {{dresscode}}",
  "de": "nicht ohne {{dresscode}}"
}
```
German correctly omits article in this prepositional phrase.

### 2. Formality Level (Sie vs. Du)

**Current implementation uses informal "du" throughout:**
- Consistent with event/community app context
- Appropriate for younger, casual audience
- Should be maintained across all future translations

**If formality needs to change:**
- Must be consistent across ALL strings
- Affects pronouns, verb forms, and possessives
- Could implement as user preference setting
- Example: `"Dein Konto"` (du) vs `"Ihr Konto"` (Sie)

### 3. Compound Words

**German uses compound words, English uses separate words:**
- DE: `"Sonnenaufgang"` (sun-rise as one word)
- EN: `"sunrise"` (often one word in English too)
- DE: `"Verkehrsmitteln"` (transport-means as compound)
- EN: `"public transport"` (separate words)

**Best practice:** Let native speakers guide compound word formation in German.

### 4. False Friends Warning

Common German-English false friends to avoid:
- `"eventuell"` (DE) = "possibly" (EN), NOT "eventually"
- `"aktuell"` (DE) = "current" (EN), NOT "actual"
- `"sensibel"` (DE) = "sensitive" (EN), NOT "sensible"

### 5. Label Length Considerations

**German text is typically 30-50% longer than English:**
- EN: `"Settings"` (8 chars)
- DE: `"Einstellungen"` (14 chars)

**Design implications:**
- Use flexible CSS (avoid fixed widths)
- Test UI with longest language
- Allow text wrapping where appropriate
- Use icons + text for space-constrained areas

### 6. Cultural Context

**Time expressions should match local conventions:**
- DE: `"bis Sonntag zur besten Sendezeit"` ✅ (idiomatic)
- EN: `"til Sunday's primetime"` ⚠️ (acceptable but could be more natural)

**Distance/transport references:**
- Consider regional differences (public transport availability varies)
- Current: `"within 30 min public transport"` (generic, works globally)

## Technical Implementation Best Practices

### 1. Translation File Structure

**Always maintain identical structure across languages:**
```json
{
  "_comment": "Language name and metadata",
  "_language": {
    "code": "en",
    "name": "English",
    "native_name": "English"
  },
  
  "filter_bar": { /* ... */ },
  "dashboard": { /* ... */ },
  "map": { /* ... */ },
  "categories": { /* ... */ },
  "common": { /* ... */ }
}
```

### 2. Adding New Translation Keys

**Checklist when adding a new translatable string:**
1. Add to `en.json` (English source)
2. Add to `de.json` (German translation)
3. Add to `cs.json` (Czech translation)
4. Use same nested structure in all three files
5. Test with all three languages in browser
6. Run feature verifier: `python3 src/modules/feature_verifier.py --verbose`

### 3. Variable Interpolation

**Use consistent `{{variable}}` syntax:**
```json
{
  "en": "within {{distance}} km",
  "de": "innerhalb {{distance}} km",
  "cs": "do {{distance}} km"
}
```

**In code:**
```javascript
const text = this.i18n.t('filter_bar.distance_filters.within_km', { distance: 5 });
// Result: "within 5 km" / "innerhalb 5 km" / "do 5 km"
```

### 4. Testing Translations

**Manual testing checklist:**
- [ ] Visit `/` (default language)
- [ ] Visit `/en` (English)
- [ ] Visit `/de` (German)
- [ ] Visit `/cs` (Czech)
- [ ] Visit `/de/hof` (language + region combo)
- [ ] Test language switcher in dashboard menu
- [ ] Check localStorage persistence (refresh page)
- [ ] Verify all UI elements render without overflow
- [ ] Test with browser DevTools mobile view (smaller screens)

**Automated testing:**
```bash
# Verify translation key completeness
python3 tests/test_translations.py --verbose

# Verify feature registry
python3 src/modules/feature_verifier.py --verbose
```

### 5. Config Settings

**Root-level language config (config.json):**
```json
{
  "defaultLanguage": "de",
  "_comment_defaultLanguage": "Default language when no region-specific language is set",
  "supportedLanguages": ["de", "en", "cs"],
  "_comment_supportedLanguages": "Languages available for UI and content translations"
}
```

**Region-specific language config (currently not implemented in code):**
```json
{
  "regions": {
    "antarctica": {
      "defaultLanguage": "en"
    },
    "hof": {
      "defaultLanguage": "de"
    }
  }
}
```

**⚠️ Note:** Region-specific `defaultLanguage` is defined but NOT used by `i18n.js`. To implement:
1. Update `app.js` → `applyRegionFromUrl()` to check region config
2. Pass region language preference to `i18n.init()`
3. Update language detection priority in `i18n.js` → `detectLanguage()`

## Using Free AI Tools for Translation

### Recommended Tools

1. **DuckDuckGo AI Chat (chat.duckduckgo.com)**
   - Free, no account required
   - Good for translation quality checks
   - Can validate natural phrasing

2. **DeepL Free (deepl.com)**
   - Best for German/English translation
   - More natural than Google Translate
   - Free tier: 500,000 chars/month

3. **Claude/ChatGPT Free Tiers**
   - Good for batch translation validation
   - Can check context and nuance
   - Helpful for identifying false friends

### Translation Workflow with AI

**For new features requiring translations:**

1. **Write English source text first** (most developers comfortable with English)

2. **Get AI translation:**
   ```
   Prompt: "Translate this to natural, informal German for a community events app.
   Maintain any {{variables}} exactly as written. Context: [describe UI element]
   
   English: 'Find events within {{distance}} km from your location'
   German: ?"
   ```

3. **Validate with native speaker** (if possible)

4. **Cross-reference with existing translations** (maintain consistency)

5. **Test in UI** (check length, readability, cultural fit)

### AI Translation Validation

**Use AI to check existing translations:**
```
Prompt: "Is this German translation natural and idiomatic for a casual events app?

EN: 'til Sunday's primetime'
DE: 'bis Sonntag zur besten Sendezeit'

Should I change anything? Consider:
- Formality (we use 'du' not 'Sie')
- Natural phrasing for German speakers
- Context: time filter for event search"
```

**Key questions to ask AI:**
- Is the formality level consistent?
- Are there any false friends or awkward phrases?
- Does the German text flow naturally?
- Is the meaning identical to English?
- Are there better idiomatic alternatives?

## Common Translation Scenarios

### 1. Time-Related Phrases

**Pattern: Relative time expressions**
```json
{
  "en": "in the next 6 hours",
  "de": "in den nächsten 6 Stunden"
}
```

**Pattern: Until/til constructions**
```json
{
  "en": "til sunrise",
  "de": "bis Sonnenaufgang"
}
```

### 2. Distance/Location Phrases

**Pattern: "within X" constructions**
```json
{
  "en": "within 30 min walk",
  "de": "innerhalb 30 Min. zu Fuß"
}
```

**Pattern: "from X" constructions**
```json
{
  "en": "from here",
  "de": "von hier"
}
```

### 3. UI Actions

**Pattern: Loading states**
```json
{
  "en": "Loading...",
  "de": "Lädt..."
}
```

**Pattern: Unknown/fallback states**
```json
{
  "en": "unknown",
  "de": "unbekannt"
}
```

## Accessibility (a11y) Considerations

### 1. Language Attribute

**Always set `<html lang="XX">` based on current language:**
```javascript
// In i18n.js init() method:
document.documentElement.lang = this.currentLang;
```

**Impact:**
- Screen readers pronounce text correctly
- Browser translation tools work better
- Search engines index correctly

### 2. ARIA Labels

**ARIA labels MUST be translated:**
```json
{
  "aria_labels": {
    "en": {
      "open_menu": "Open application menu",
      "close_menu": "Close application menu"
    },
    "de": {
      "open_menu": "Anwendungsmenü öffnen",
      "close_menu": "Anwendungsmenü schließen"
    }
  }
}
```

**Why it matters:**
- Screen reader users navigate in their language
- WCAG 2.1 AA compliance requires proper language markup
- Improves user experience for non-visual users

### 3. Alt Text for Icons

**Icon labels should be translatable:**
```javascript
// Good: Translatable icon label
<button aria-label="{{ i18n.t('aria_labels.open_menu') }}">
  <i data-lucide="menu"></i>
</button>

// Bad: Hardcoded English label
<button aria-label="Open menu">
  <i data-lucide="menu"></i>
</button>
```

## Troubleshooting

### Issue: New translation not showing

**Checklist:**
1. Clear browser cache (`Ctrl+Shift+R`)
2. Check browser console for load errors
3. Verify JSON syntax (use `jq` or JSON validator)
4. Confirm key exists in ALL language files
5. Check that translation file was rebuilt into `public/index.html`
6. Run: `python3 src/event_manager.py generate`

### Issue: Wrong language displayed

**Debug steps:**
1. Check URL path (should be `/de` or `/en`)
2. Check localStorage: `localStorage.getItem('krwl_language')`
3. Clear localStorage: `localStorage.clear()`
4. Check browser language setting
5. Verify `config.json` has correct `defaultLanguage`
6. Check console for i18n initialization logs

### Issue: Variable interpolation not working

**Common causes:**
```javascript
// ❌ Wrong: Using wrong variable name
this.i18n.t('filter_bar.distance_filters.within_km', { dist: 5 });
// Should be: { distance: 5 }

// ✅ Correct: Variable name matches template
this.i18n.t('filter_bar.distance_filters.within_km', { distance: 5 });
```

**Check translation file:**
```json
{
  "within_km": "within {{distance}} km"
  // Variable must be "distance", not "dist" or other name
}
```

## Future Enhancements

### 1. Region-Specific Language Detection

**Implement in app.js:**
```javascript
detectLanguageFromRegion(regionId) {
    const region = this.config.regions[regionId];
    if (region && region.defaultLanguage) {
        return region.defaultLanguage;
    }
    return this.config.defaultLanguage || 'en';
}
```

### 2. Language Switcher Persistence in URL

**Enhance language switching:**
- When user changes language in dashboard
- Update URL to reflect new language (`/en` → `/de`)
- Preserve region if present (`/en/hof` → `/de/hof`)
- Maintain scroll position and filters

### 3. Smarter Fallback Chain

**Improve fallback logic:**
```
Missing translation → Try region language → Try browser language → English
```

### 4. Date/Time Localization

**Add locale-specific formatting:**
```javascript
// Use Intl API for dates
const formatter = new Intl.DateTimeFormat(this.currentLang, {
    weekday: 'long',
    year: 'numeric',
    month: 'long',
    day: 'numeric'
});
```

### 5. Pluralization Rules

**Add proper plural forms:**
```json
{
  "event_count": {
    "en": {
      "one": "1 event",
      "other": "{{count}} events"
    },
    "de": {
      "one": "1 Veranstaltung",
      "other": "{{count}} Veranstaltungen"
    }
  }
}
```

## Resources

### Documentation
- KRWL> Feature Registry: `features.json` → `multilanguage-support`
- Translation Files: `assets/json/translations/*.json`
- i18n Module: `assets/js/i18n.js`
- Config: `config.json` → `defaultLanguage`, `supportedLanguages`

### Testing
- Feature Verifier: `python3 src/modules/feature_verifier.py --verbose`
- Translation Tests: `python3 tests/test_translations.py --verbose`

### External Resources
- German Grammar: [canoo.net](https://www.canoo.net/)
- Translation Quality: [DeepL](https://www.deepl.com/)
- i18n Best Practices: [W3C Internationalization](https://www.w3.org/International/)
- WCAG Language Requirements: [WCAG 2.1 Language of Page](https://www.w3.org/WAI/WCAG21/Understanding/language-of-page.html)

---

**Last Updated:** February 2026  
**Maintained by:** KRWL> Development Team  
**Questions?** Check `features.json` or run `python3 src/event_manager.py --help`
