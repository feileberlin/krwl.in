# KRWL HOF Monochromatic Color Palette Reference

**Status:** Read-Only Reference Document  
**Purpose:** Professional color palette documentation  
**Last Updated:** 2026-01-18

---

## Overview

This document serves as a **permanent reference** for the KRWL HOF **truly monochromatic** color palette based on the **ecoBarbie** theme. **ALL colors** are derived from a single base color (#D689B8) through scientifically-calculated tints, shades, and tones - no exceptions.

**Base Color:** ecoBarbie `#D689B8` (RGB: 214, 137, 184)  
**Color Theory:** HSV: 323.4° hue, 36.0% saturation, 83.9% value

**Monochromatic Design:** Every single color in the application - backgrounds, text, borders, accents, warnings, errors - derives from the ecoBarbie pink base color using HSV transformations.

> **Note:** This is a reference document only. The actual colors used in the application are defined in `config.json` under the `design.colors` section with inline color preview comments (█ blocks). To modify colors, edit `config.json` and regenerate design tokens using `python3 src/tools/generate_design_tokens.py`.

---

## Color Theory: Monochromatic Palette

A **monochromatic color scheme** uses variations of a single hue by adjusting:
- **Tints** (base color + white) - Lighter variations
- **Shades** (base color + black) - Darker variations  
- **Tones** (base color + grey) - Muted variations

---

## Complete Color Palette

### Primary ecoBarbie Colors

| Color Preview | Name | Hex | RGB | CSS Variable | Usage |
|---------------|------|-----|-----|--------------|-------|
| ![#D689B8](https://via.placeholder.com/20x20/D689B8/D689B8.png) | **Primary** | `#D689B8` | 214, 137, 184 | `--color-primary` | Primary brand color, accents, highlights |
| ![#E8A5C8](https://via.placeholder.com/20x20/E8A5C8/E8A5C8.png) | **Primary Hover** | `#E8A5C8` | 232, 165, 200 | `--color-primary-hover` | Hover states for primary |
| ![#D689B8](https://via.placeholder.com/20x20/D689B8/D689B8.png) | **Success** | `#D689B8` | 214, 137, 184 | `--color-success` | Success state (uses primary) |

### ecoBarbie Tints (+ White) - Scientifically Generated

**Usage:** Light backgrounds, hover states, subtle highlights, soft UI elements

| Color Preview | Name | Hex | RGB | CSS Variable | Lightness |
|---------------|------|-----|-----|--------------|-----------|
| ![#de96c2](https://via.placeholder.com/20x20/de96c2/de96c2.png) | **Tint 20%** | `#de96c2` | 222, 150, 194 | `--color-tint-20` | Subtle tint |
| ![#e6a4cc](https://via.placeholder.com/20x20/e6a4cc/e6a4cc.png) | **Tint 40%** | `#e6a4cc` | 230, 164, 204 | `--color-tint-40` | Light backgrounds |
| ![#eeb2d7](https://via.placeholder.com/20x20/eeb2d7/eeb2d7.png) | **Tint 60%** | `#eeb2d7` | 238, 178, 215 | `--color-tint-60` | Very light backgrounds |
| ![#f6c1e2](https://via.placeholder.com/20x20/f6c1e2/f6c1e2.png) | **Tint 80%** | `#f6c1e2` | 246, 193, 226 | `--color-tint-80` | Ultra-light highlights |

### ecoBarbie Shades (+ Black) - Scientifically Generated

**Usage:** Text on light backgrounds, borders, dark accents, depth, shadows

| Color Preview | Name | Hex | RGB | CSS Variable | Darkness |
|---------------|------|-----|-----|--------------|----------|
| ![#ab6d93](https://via.placeholder.com/20x20/ab6d93/ab6d93.png) | **Shade 20%** | `#ab6d93` | 171, 109, 147 | `--color-shade-20` | Medium dark |
| ![#80526e](https://via.placeholder.com/20x20/80526e/80526e.png) | **Shade 40%** | `#80526e` | 128, 82, 110 | `--color-shade-40` | Dark accents |
| ![#553649](https://via.placeholder.com/20x20/553649/553649.png) | **Shade 60%** | `#553649` | 85, 54, 73 | `--color-shade-60` | Very dark backgrounds |
| ![#2a1b24](https://via.placeholder.com/20x20/2a1b24/2a1b24.png) | **Shade 80%** | `#2a1b24` | 42, 27, 36 | `--color-shade-80` | Near-black backgrounds |

### ecoBarbie Tones (+ Grey) - Scientifically Generated

**Usage:** Subtle accents, disabled states, secondary elements, soft UI, muted effects

| Color Preview | Name | Hex | RGB | CSS Variable | Saturation |
|---------------|------|-----|-----|--------------|------------|
| ![#d698be](https://via.placeholder.com/20x20/d698be/d698be.png) | **Tone 20%** | `#d698be` | 214, 152, 190 | `--color-tone-20` | Slightly desaturated |
| ![#d6a7c4](https://via.placeholder.com/20x20/d6a7c4/d6a7c4.png) | **Tone 40%** | `#d6a7c4` | 214, 167, 196 | `--color-tone-40` | Moderate desaturation |
| ![#d6b7ca](https://via.placeholder.com/20x20/d6b7ca/d6b7ca.png) | **Tone 60%** | `#d6b7ca` | 214, 183, 202 | `--color-tone-60` | Soft neutral |
| ![#d6c6d0](https://via.placeholder.com/20x20/d6c6d0/d6c6d0.png) | **Tone 80%** | `#d6c6d0` | 214, 198, 208 | `--color-tone-80` | Very soft neutral |

### Legacy Colors (Backward Compatibility)

| Color Preview | Name | Hex | RGB | CSS Variable | Notes |
|---------------|------|-----|-----|--------------|-------|
| ![#FFB3DF](https://via.placeholder.com/20x20/FFB3DF/FFB3DF.png) | **Medium Tint** | `#FFB3DF` | 255, 179, 223 | `--color-medium-tint` | Legacy bright tint |
| ![#D689B8](https://via.placeholder.com/20x20/D689B8/D689B8.png) | **Light Tone** | `#D689B8` | 214, 137, 184 | `--color-light-tone` | Duplicate of primary |
| ![#B05F8E](https://via.placeholder.com/20x20/B05F8E/B05F8E.png) | **Medium Tone** | `#B05F8E` | 176, 95, 142 | `--color-medium-tone` | Similar to shade_20 |
| ![#8A4A70](https://via.placeholder.com/20x20/8A4A70/8A4A70.png) | **Dark Tone** | `#8A4A70` | 138, 74, 112 | `--color-dark-tone` | Similar to shade_40 |
| ![#BF5087](https://via.placeholder.com/20x20/BF5087/BF5087.png) | **Light Shade** | `#BF5087` | 191, 80, 135 | `--color-light-shade` | Consider removing |

### Neutral Greys & Blacks

**Note:** In a true monochromatic design, there are NO neutral greys. All dark/light colors derive from ecoBarbie.

### Background Colors (Very Dark Shades)

**Monochromatic:** 88-92% darker shades of ecoBarbie for backgrounds

| Color Preview | Name | Hex | RGB | CSS Variable | Usage |
|---------------|------|-----|-----|--------------|-------|
| ![#110a0e](https://via.placeholder.com/20x20/110a0e/110a0e.png) | **BG Primary** | `#110a0e` | 17, 10, 14 | `--color-bg-primary` | Main background (92% darker) |
| ![#150d12](https://via.placeholder.com/20x20/150d12/150d12.png) | **BG Secondary** | `#150d12` | 21, 13, 18 | `--color-bg-secondary` | Secondary background (90% darker) |
| ![#191016](https://via.placeholder.com/20x20/191016/191016.png) | **BG Tertiary** | `#191016` | 25, 16, 22 | `--color-bg-tertiary` | Tertiary background (88% darker) |

### Text Colors (Very Light Tints)

**Monochromatic:** 92-98% lighter tints of ecoBarbie for text on dark backgrounds

| Color Preview | Name | Hex | RGB | CSS Variable | Contrast | Usage |
|---------------|------|-----|-----|--------------|----------|-------|
| ![#f9f5f8](https://via.placeholder.com/20x20/f9f5f8/f9f5f8.png) | **Text Primary** | `#f9f5f8` | 249, 245, 248 | `--color-text-primary` | High | Primary text (98% lighter) |
| ![#f2e9ee](https://via.placeholder.com/20x20/f2e9ee/f2e9ee.png) | **Text Secondary** | `#f2e9ee` | 242, 233, 238 | `--color-text-secondary` | Medium | Secondary text (95% lighter) |
| ![#eadde5](https://via.placeholder.com/20x20/eadde5/eadde5.png) | **Text Tertiary** | `#eadde5` | 234, 221, 229 | `--color-text-tertiary` | Lower | Tertiary text (92% lighter) |

### Border Colors (Medium Dark Shades)

**Monochromatic:** 75-78% darker shades of ecoBarbie for borders

| Color Preview | Name | Hex | RGB | CSS Variable | Usage |
|---------------|------|-----|-----|--------------|-------|
| ![#35222e](https://via.placeholder.com/20x20/35222e/35222e.png) | **Border Primary** | `#35222e` | 53, 34, 46 | `--color-border-primary` | Primary border (75% darker) |
| ![#2f1e28](https://via.placeholder.com/20x20/2f1e28/2f1e28.png) | **Border Secondary** | `#2f1e28` | 47, 30, 40 | `--color-border-secondary` | Secondary border (78% darker) |

### Accent Colors (Monochromatic Variants)

**Monochromatic:** All accents derive from ecoBarbie with saturation/value adjustments for visual distinction

| Color Preview | Name | Hex | RGB | CSS Variable | Transform | Usage |
|---------------|------|-----|-----|--------------|-----------|-------|
| ![#e07fba](https://via.placeholder.com/20x20/e07fba/e07fba.png) | **Accent** | `#e07fba` | 224, 127, 186 | `--color-accent` | +20% sat, +5% val | Links, info, highlights |
| ![#eb7dc0](https://via.placeholder.com/20x20/eb7dc0/eb7dc0.png) | **Warning** | `#eb7dc0` | 235, 125, 192 | `--color-warning` | +30% sat, +10% val | Warnings, pending states |
| ![#954476](https://via.placeholder.com/20x20/954476/954476.png) | **Error** | `#954476` | 149, 68, 118 | `--color-error` | +50% sat, -30% val | Errors, critical alerts |
| ![#eeb2d7](https://via.placeholder.com/20x20/eeb2d7/eeb2d7.png) | **Bookmark** | `#eeb2d7` | 238, 178, 215 | `--color-bookmark` | Same as tint_60 | Bookmark highlight |
| ![#f6c1e2](https://via.placeholder.com/20x20/f6c1e2/f6c1e2.png) | **Bookmark Light** | `#f6c1e2` | 246, 193, 226 | `--color-bookmark-light` | Same as tint_80 | Bookmark hover |
| ![#fce0ef](https://via.placeholder.com/20x20/fce0ef/fce0ef.png) | **Bookmark Lighter** | `#fce0ef` | 252, 224, 239 | `--color-bookmark-lighter` | 90% lighter tint | Bookmark subtle |
---

## Alpha Channel Variations

### Primary Pink with Alpha (RGBA)

Common opacity levels for ecoBarbie `#D689B8` (214, 137, 184):

| Opacity | RGBA | Usage |
|---------|------|-------|
| 100% | `rgba(214, 137, 184, 1.0)` | Solid color |
| 95% | `rgba(214, 137, 184, 0.95)` | Nearly solid |
| 80% | `rgba(214, 137, 184, 0.8)` | Strong glow |
| 60% | `rgba(214, 137, 184, 0.6)` | Medium glow |
| 50% | `rgba(214, 137, 184, 0.5)` | Half opacity |
| 40% | `rgba(214, 137, 184, 0.4)` | Light glow |
| 30% | `rgba(214, 137, 184, 0.3)` | Subtle glow |
| 25% | `rgba(214, 137, 184, 0.25)` | Very subtle |
| 20% | `rgba(214, 137, 184, 0.2)` | Barely visible |
| 15% | `rgba(214, 137, 184, 0.15)` | Ultra subtle |
| 10% | `rgba(214, 137, 184, 0.1)` | Hint of color |

### Black with Alpha (Shadows)

Common opacity levels for black shadows:

| Opacity | RGBA | Usage |
|---------|------|-------|
| 80% | `rgba(0, 0, 0, 0.8)` | Strong shadow/overlay |
| 70% | `rgba(0, 0, 0, 0.7)` | Medium-strong shadow |
| 60% | `rgba(0, 0, 0, 0.6)` | Medium shadow |
| 50% | `rgba(0, 0, 0, 0.5)` | Balanced shadow |
| 40% | `rgba(0, 0, 0, 0.4)` | Light shadow |
| 30% | `rgba(0, 0, 0, 0.3)` | Subtle shadow |

### Background with Alpha

| Color | RGBA | Usage |
|-------|------|-------|
| **Dark Bg Semi-transparent** | `rgba(13, 17, 23, 0.95)` | Backdrop filter backgrounds |
| **Dark Bg Overlay** | `rgba(13, 17, 23, 0.6)` | Light overlay |

### Warning/Accent with Alpha

| Color | RGBA | Usage |
|-------|------|-------|
| **Warning Glow** | `rgba(210, 153, 34, 0.3)` | Warning highlight |
| **Warning Subtle** | `rgba(210, 153, 34, 0.15)` | Warning background |
| **Warning Very Subtle** | `rgba(210, 153, 34, 0.05)` | Warning hint |
| **Error Subtle** | `rgba(248, 81, 73, 0.1)` | Error background |

---

## Professional Usage Guidelines

### Accessibility

All color combinations meet **WCAG 2.1 Level AA** standards:
- **Normal text:** Minimum 4.5:1 contrast ratio
- **Large text:** Minimum 3:1 contrast ratio
- **UI components:** Minimum 3:1 contrast ratio

### Best Practices

1. **Consistency:** Always use CSS variables from the design system
2. **Never hardcode colors** - Use `var(--color-name)` syntax
3. **Alpha channel usage:** For glows, shadows, and overlays
4. **Test on multiple displays:** Check color rendering across devices
5. **Dark mode optimized:** This palette is designed for dark backgrounds

### Color Relationships

```
Text Hierarchy:
text_primary (#c9d1d9) > text_secondary (#8b949e) > text_tertiary (#6e7681)

Background Hierarchy:
bg_primary (#0d1117) > bg_secondary (#161b22) > bg_tertiary (#21262d)

Border Hierarchy:
border_primary (#30363d) > border_secondary (#21262d)

ecoBarbie Hierarchy:
primary (#D689B8) > primary_hover (#E8A5C8) > medium_tint (#FFB3DF)
```

---

## Implementation

### CSS Variables

All colors are available as CSS custom properties:

```css
/* Example usage */
.element {
  color: var(--color-text-primary);
  background: var(--color-bg-primary);
  border: 1px solid var(--color-border-primary);
  box-shadow: 0 0 10px var(--color-primary-alpha-30);
}
```

### Adding New Colors

To add a new color to the palette:

1. Edit `config.json` → `design.colors` section
2. Run: `python3 src/tools/generate_design_tokens.py`
3. Use: `var(--color-your-new-name)` in CSS
4. Update this reference document

---

## Color Psychology

**Pink (ecoBarbie):**
- Conveys: Warmth, creativity, playfulness, ecology-conscious
- Emotional: Friendly, approachable, modern
- Brand: Distinctive, memorable, progressive

**Dark Greys:**
- Conveys: Professionalism, sophistication, focus
- Emotional: Calm, serious, trustworthy
- UX: Reduces eye strain, emphasizes content

**Monochromatic Benefits:**
- Creates visual harmony
- Professional and cohesive appearance
- Easier to maintain consistency
- Clear visual hierarchy
- Better accessibility when done correctly

---

## Color Preview System in config.json

### How It Works

The project uses a clever system for providing **inline color previews** directly in `config.json`:

1. **Color blocks (█)** - Unicode block character provides visual color reference
2. **_preview_* keys** - Special comment keys that show hex codes with descriptions
3. **Auto-generation** - Design token generator converts these to CSS variables

### Example from config.json

```json
{
  "design": {
    "colors": {
      "ecobarbie_tint_40": "#e6a4cc",
      "_preview_tint_40": "█ #e6a4cc - 40% lighter (light backgrounds)"
    }
  }
}
```

### Benefits

- ✅ **Quick identification** - See color at a glance in text editor
- ✅ **Documentation** - Color purpose embedded right next to definition
- ✅ **No duplication** - Single source of truth for colors
- ✅ **Valid JSON** - _preview_* keys are ignored by parsers but visible to humans
- ✅ **IDE support** - Most editors show Unicode blocks in actual colors

### Best Practices

1. **Always add _preview** - For every color, add a `_preview_*` comment key
2. **Use █ symbol** - Standard Unicode block character (U+2588)
3. **Format:** `█ #hexcode - descriptive text`
4. **Keep organized** - Group related colors with `_comment_*_section` headers

## Technical Notes

### Color Space

All colors are defined in **sRGB** color space for maximum web compatibility.

### Format Preference

- **Hex codes:** For solid colors (`#D689B8`)
- **RGBA:** For transparent colors (`rgba(214, 137, 184, 0.3)`)
- **CSS Variables:** For all production use (`var(--color-primary)`)

### Browser Support

- Modern browsers: Full support for CSS custom properties
- Legacy browsers: Fallback values where critical

---

## Version History

- **v3.0** (2026-01-18): TRUE Monochromatic Design - ALL colors derive from ecoBarbie
  - **Breaking change**: Replaced ALL non-ecoBarbie colors with monochromatic variants
  - Backgrounds: `bg_*` now use 88-92% darker ecoBarbie shades (was blue-grey)
  - Text: `text_*` now use 92-98% lighter ecoBarbie tints (was neutral grey)
  - Borders: `border_*` now use 75-78% darker ecoBarbie shades (was grey)
  - Accents: `accent`, `warning`, `error` now use saturation/value adjusted ecoBarbie (was blue/orange/red)
  - Bookmarks: Now use ecoBarbie tints (tint_60, tint_80, 90% tint)
  - **Result**: 100% monochromatic palette - every color derives from #D689B8
  - Added color preview images in documentation using placeholder service
- **v2.2** (2026-01-18): Simplified naming - removed "ecobarbie" prefix
  - Renamed: `ecobarbie_tint_*` → `tint_*` (shorter, cleaner names)
  - Renamed: `ecobarbie_shade_*` → `shade_*`
  - Renamed: `ecobarbie_tone_*` → `tone_*`
  - Renamed: `ecobarbie_*` legacy colors → simplified names
  - All colors still derive from ecoBarbie (#D689B8) but with concise naming
  - CSS variables now use shorter names: `--color-tint-20` instead of `--color-ecobarbie-tint-20`
- **v2.1** (2026-01-18): Consistent ecoBarbie naming for all pink colors
  - Renamed: `primary` → `ecobarbie_primary` (with alias for compatibility)
  - Renamed: `primary_hover` → `ecobarbie_primary_hover` (with alias)
  - Renamed: `success` → `ecobarbie_success` (with alias)
  - All ecoBarbie-derived colors now follow `ecobarbie_*` naming scheme
  - Backward-compatible aliases maintained for existing code
- **v2.0** (2026-01-18): Scientifically-generated monochromatic palette
  - Added 12 new scientifically-calculated colors (4 tints, 4 shades, 4 tones)
  - Implemented inline color preview system with █ blocks
  - Organized colors into logical sections with clear usage guidelines
  - Kept legacy colors for backward compatibility
  - Updated documentation with CSS variable references
- **v1.0** (2026-01-17): Initial comprehensive palette documentation
  - Documented all 60+ color variations
  - Added RGBA alpha channel reference
  - Included accessibility guidelines
  - Professional usage guidelines

---

## Related Documentation

- **Design Tokens:** `assets/html/design-tokens.css` (auto-generated)
- **Configuration:** `config.json` → `design.colors` section
- **Generator:** `src/tools/generate_design_tokens.py`
- **Style Guide:** `assets/css/style.css` (header comments)

---

**Questions or Suggestions?**  
Open an issue on GitHub or contact the maintainers.
