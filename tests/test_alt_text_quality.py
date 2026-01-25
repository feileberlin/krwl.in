#!/usr/bin/env python3
"""
Runtime Validation Test for Alt Text Quality

This test validates the QUALITY of alt text in generated HTML, not just existence.
It catches issues that regex-based linting misses, such as:
- Generic alt text ("marker", "image", "icon")
- Missing context (no event title in event markers)
- Empty or whitespace-only alt text
- Alt text that doesn't match the marker's purpose

Run this test after generating HTML to ensure accessibility standards.
"""

import sys
import re
from pathlib import Path
from typing import List, Tuple, Dict

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))


def parse_html_for_img_tags(html_content: str) -> List[Dict[str, str]]:
    """
    Extract all img tags with their alt text from HTML.
    Returns list of dicts with: {'tag': full_tag, 'alt': alt_value, 'src': src_value}
    """
    img_tags = []
    # Match img tags with alt attributes
    img_pattern = r'<img\s+([^>]*?)>'
    
    for match in re.finditer(img_pattern, html_content, re.IGNORECASE):
        full_tag = match.group(0)
        attrs = match.group(1)
        
        # Extract alt attribute
        alt_match = re.search(r'alt\s*=\s*["\']([^"\']*)["\']', attrs, re.IGNORECASE)
        alt_value = alt_match.group(1) if alt_match else None
        
        # Extract src attribute for context
        src_match = re.search(r'src\s*=\s*["\']([^"\']*)["\']', attrs, re.IGNORECASE)
        src_value = src_match.group(1) if src_match else None
        
        img_tags.append({
            'tag': full_tag,
            'alt': alt_value,
            'src': src_value[:50] + '...' if src_value and len(src_value) > 50 else src_value
        })
    
    return img_tags


def check_generic_alt_text(alt_text: str) -> Tuple[bool, str]:
    """
    Check if alt text is generic/unhelpful.
    Returns (is_generic, reason)
    """
    if not alt_text:
        return True, "Alt text is empty or missing"
    
    alt_lower = alt_text.lower().strip()
    
    # Check for whitespace-only
    if not alt_lower:
        return True, "Alt text is whitespace-only"
    
    # Generic patterns that should be flagged
    generic_patterns = [
        (r'^marker$', "Just 'marker' - no context"),
        (r'^icon$', "Just 'icon' - no context"),
        (r'^image$', "Just 'image' - no context"),
        (r'^picture$', "Just 'picture' - no context"),
        (r'^\s*event\s+marker\s*$', "Generic 'event marker' - missing event details"),
        (r'^\s*\w+\s+event\s+marker\s*$', "Category-only marker - missing event title (e.g., 'music event marker')"),
        (r'^location\s+marker$', "Generic 'location marker' - no context about which location"),
    ]
    
    for pattern, reason in generic_patterns:
        if re.match(pattern, alt_lower):
            return True, reason
    
    return False, ""


def check_marker_alt_text_quality(alt_text: str, is_event_marker: bool = True) -> Tuple[bool, List[str]]:
    """
    Check if marker alt text meets quality standards.
    Returns (passes, list_of_issues)
    """
    issues = []
    
    if not alt_text:
        issues.append("Missing alt text")
        return False, issues
    
    # Check for generic patterns
    is_generic, generic_reason = check_generic_alt_text(alt_text)
    if is_generic:
        issues.append(f"Generic alt text: {generic_reason}")
    
    if is_event_marker:
        # Event markers should include both event title and category
        # Expected format: "Event Title - category marker"
        if ' - ' not in alt_text:
            issues.append("Event marker missing ' - ' separator between title and category")
        
        if not alt_text.endswith(' marker'):
            issues.append("Event marker should end with ' marker'")
        
        # Check if it has meaningful title (not just "Event")
        if alt_text.startswith('Event - ') and alt_text != 'Event - default marker':
            # "Event - " is the fallback, but should have category
            pass
        
        # Event markers should have some descriptive text before the dash
        parts = alt_text.split(' - ')
        if len(parts) >= 2:
            title_part = parts[0].strip()
            if not title_part or title_part.lower() in ['event', 'marker', 'icon']:
                issues.append(f"Event title is generic: '{title_part}'")
    else:
        # Location markers should be descriptive
        if alt_text == 'Location marker':
            # This is the fallback - acceptable but should be rare
            pass
        elif 'marker' not in alt_text.lower():
            # Location markers should contain 'marker' for consistency
            issues.append("Location marker should contain word 'marker'")
    
    return len(issues) == 0, issues


def test_alt_text_quality():
    """
    Test that generated HTML has high-quality alt text on all markers.
    """
    print("\n" + "=" * 70)
    print("Runtime Validation: Alt Text Quality")
    print("=" * 70)
    
    base_path = Path(__file__).parent.parent
    html_file = base_path / 'public' / 'index.html'
    
    if not html_file.exists():
        print("⚠️  HTML file not found. Run 'python3 src/event_manager.py generate' first.")
        return False
    
    print(f"📄 Reading: {html_file}")
    html_content = html_file.read_text()
    
    # Extract all img tags
    img_tags = parse_html_for_img_tags(html_content)
    print(f"📊 Found {len(img_tags)} img tags in HTML")
    
    if len(img_tags) == 0:
        print("⚠️  No img tags found - this might indicate a problem with HTML generation")
        return False
    
    # Track results
    total_issues = 0
    generic_count = 0
    missing_alt_count = 0
    quality_issues = []
    
    print("\n" + "-" * 70)
    print("Analyzing Alt Text Quality:")
    print("-" * 70)
    
    for i, img_data in enumerate(img_tags, 1):
        alt_text = img_data['alt']
        src = img_data['src']
        
        # Skip if this is not a marker (e.g., logo, icons)
        # Markers are in divIcon HTML or have marker-related src
        is_likely_marker = (
            'marker' in img_data['tag'].lower() or
            'custom-marker-icon' in img_data['tag'] or
            'custom-location-marker-icon' in img_data['tag']
        )
        
        if not is_likely_marker:
            # print(f"  Skipping non-marker img tag #{i}")
            continue
        
        # Check if missing alt
        if alt_text is None:
            missing_alt_count += 1
            total_issues += 1
            print(f"\n❌ IMG #{i}: MISSING ALT TEXT")
            print(f"   Src: {src}")
            continue
        
        # Check if generic
        is_generic, generic_reason = check_generic_alt_text(alt_text)
        if is_generic:
            generic_count += 1
            total_issues += 1
            print(f"\n⚠️  IMG #{i}: GENERIC ALT TEXT")
            print(f"   Alt: '{alt_text}'")
            print(f"   Issue: {generic_reason}")
            print(f"   Src: {src}")
            quality_issues.append({
                'index': i,
                'alt': alt_text,
                'reason': generic_reason
            })
        else:
            print(f"\n✅ IMG #{i}: GOOD ALT TEXT")
            print(f"   Alt: '{alt_text}'")
    
    # Summary
    print("\n" + "=" * 70)
    print("SUMMARY:")
    print("=" * 70)
    print(f"Total img tags analyzed: {len([x for x in img_tags if 'marker' in str(x).lower()])}")
    print(f"Missing alt text: {missing_alt_count}")
    print(f"Generic alt text: {generic_count}")
    print(f"Total issues: {total_issues}")
    
    if total_issues == 0:
        print("\n🎉 All marker alt text is descriptive and accessible!")
        print("=" * 70)
        return True
    else:
        print(f"\n❌ Found {total_issues} alt text quality issues")
        print("=" * 70)
        return False


def test_event_marker_format():
    """
    Test that event markers follow the expected format:
    "Event Title - category marker"
    """
    print("\n" + "=" * 70)
    print("Format Validation: Event Markers")
    print("=" * 70)
    
    base_path = Path(__file__).parent.parent
    html_file = base_path / 'public' / 'index.html'
    
    if not html_file.exists():
        print("⚠️  HTML file not found. Run 'python3 src/event_manager.py generate' first.")
        return False
    
    html_content = html_file.read_text()
    
    # Find the addEventMarker function and extract example alt text
    # Look for the pattern: alt="${altText}"
    alt_text_pattern = r'const\s+altText\s*=\s*`([^`]+)`'
    match = re.search(alt_text_pattern, html_content)
    
    if match:
        alt_format = match.group(1)
        print(f"✓ Found alt text format in code: {alt_format}")
        
        # Verify it includes event title and category
        if '${eventTitle}' in alt_format and '${category}' in alt_format:
            print("✓ Format includes both event title and category")
            print(f"✓ Expected output example: 'Jazz Concert - music marker'")
            return True
        else:
            print("❌ Format missing required variables")
            return False
    else:
        print("⚠️  Could not find altText format in generated HTML")
        return False


def test_location_marker_format():
    """
    Test that location markers follow the expected format.
    """
    print("\n" + "=" * 70)
    print("Format Validation: Location Markers")
    print("=" * 70)
    
    base_path = Path(__file__).parent.parent
    html_file = base_path / 'public' / 'index.html'
    
    if not html_file.exists():
        print("⚠️  HTML file not found. Run 'python3 src/event_manager.py generate' first.")
        return False
    
    html_content = html_file.read_text()
    
    # Look for locationAltText definition
    location_alt_pattern = r'const\s+locationAltText\s*=\s*([^;]+);'
    match = re.search(location_alt_pattern, html_content)
    
    if match:
        alt_format = match.group(1).strip()
        print(f"✓ Found location alt text format: {alt_format}")
        
        if 'popupText' in alt_format or 'Location marker' in alt_format:
            print("✓ Format uses popup text with fallback to 'Location marker'")
            return True
        else:
            print("❌ Format missing expected pattern")
            return False
    else:
        print("⚠️  Could not find locationAltText in generated HTML")
        return False


def main():
    """Run all alt text quality tests"""
    print("\n" + "=" * 70)
    print("ALT TEXT QUALITY VALIDATION SUITE")
    print("Runtime validation for descriptive, accessible alt text")
    print("=" * 70)
    
    try:
        # Run tests
        test1 = test_event_marker_format()
        test2 = test_location_marker_format()
        test3 = test_alt_text_quality()
        
        print("\n" + "=" * 70)
        print("FINAL RESULTS:")
        print("=" * 70)
        print(f"Event Marker Format:    {'✅ PASS' if test1 else '❌ FAIL'}")
        print(f"Location Marker Format: {'✅ PASS' if test2 else '❌ FAIL'}")
        print(f"Alt Text Quality:       {'✅ PASS' if test3 else '❌ FAIL'}")
        
        if test1 and test2 and test3:
            print("\n🎉 ALL TESTS PASSED - Alt text is descriptive and accessible!")
            print("=" * 70)
            return 0
        else:
            print("\n❌ SOME TESTS FAILED - Please review alt text implementation")
            print("=" * 70)
            return 1
            
    except Exception as e:
        print(f"\n❌ Test suite error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
