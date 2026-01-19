#!/usr/bin/env python3
"""
Extract icons from marker SVGs and create icon-only versions (no gyro shape).

SIMPLE APPROACH (KISS):
1. Read all marker-*.svg files
2. Remove the standard gyro-shaped pin outline
3. Scale up the remaining content by 3x (72x72px)
4. Save back to assets/svg/ directory

Usage: python3 scripts/extract_icon_only_markers.py
"""

import os
import re
from pathlib import Path

# Configuration
BASE_DIR = Path(__file__).parent.parent
MARKER_DIR = BASE_DIR / 'assets' / 'svg'
SCALE_FACTOR = 3  # 3x larger
ORIGINAL_SIZE = (32, 48)  # Original marker size
NEW_SIZE = (96, 96)  # Square icon, 3x scale of 32px width
COLOR = "#D689B8"  # ecoBarbie color

def remove_gyro_outline(svg_content):
    """Remove the gyro-shaped pin outline from marker SVG."""
    # Remove the standard gyro shape path
    # Pattern: <path d="M16 2 C9 2 3 8 3 15 C3 24 16 46 16 46 C16 46 29 24 29 15 C29 8 23 2 16 2 Z".../>
    svg_content = re.sub(
        r'<path d="M16 2\s+C9 2 3 8 3 15\s+C3 24 16 46 16 46\s+C16 46 29 24 29 15\s+C29 8 23 2 16 2\s+Z"[^>]*/>',
        '',
        svg_content,
        flags=re.DOTALL
    )
    
    # Also remove any "STANDARD GYRO SHAPE" comment
    svg_content = re.sub(r'<!--\s*STANDARD GYRO SHAPE.*?-->', '', svg_content, flags=re.DOTALL)
    
    return svg_content

def scale_svg_3x(svg_content):
    """Scale SVG from 32x48 to 96x96 (3x) and center the icon."""
    
    # Remove gyro outline first
    svg_content = remove_gyro_outline(svg_content)
    
    # Update viewBox and dimensions
    svg_content = re.sub(
        r'viewBox="0 0 32 48"',
        f'viewBox="0 0 {NEW_SIZE[0]} {NEW_SIZE[1]}"',
        svg_content
    )
    
    svg_content = re.sub(
        r'width="32"',
        f'width="{NEW_SIZE[0]}"',
        svg_content
    )
    
    svg_content = re.sub(
        r'height="48"',
        f'height="{NEW_SIZE[1]}"',
        svg_content
    )
    
    # Scale and center the icon content
    # Original content was centered around (16, ~15-20) in 32x48 viewBox
    # New viewBox is 96x96, so center is at (48, 48)
    # Scale factor is 3x, so we need to scale and translate
    
    # Find the content after drop shadow and before </svg>
    # Note: ellipse is self-closing, so it's <ellipse .../> not </ellipse>
    match = re.search(r'(<!-- Drop shadow -->.*?<ellipse[^>]*/>)(.*)(</svg>)', svg_content, re.DOTALL)
    
    if match:
        drop_shadow_part = match.group(1)
        icon_content = match.group(2).strip()
        closing_tag = match.group(3)
        
        # Scale the drop shadow position and size
        new_drop_shadow = f'''<!-- Drop shadow for depth -->
  <ellipse cx="{NEW_SIZE[0]/2}" cy="{NEW_SIZE[1]-6}" rx="{NEW_SIZE[0]/5}" ry="{NEW_SIZE[1]/16}" fill="#000" opacity="0.3"/>'''
        
        # Wrap icon content in a scaled and centered group
        # Offset to center: original (16, 15) -> new (48, 48)
        # We scale by 3, so translate by (48 - 16*3, 48 - 15*3) = (0, 3)
        centered_content = f'''
  
  <!-- Icon content scaled 3x and centered -->
  <g transform="translate({NEW_SIZE[0]/2 - 16*SCALE_FACTOR}, {NEW_SIZE[1]/2 - 15*SCALE_FACTOR}) scale({SCALE_FACTOR})">
{icon_content}
  </g>'''
        
        svg_content = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {NEW_SIZE[0]} {NEW_SIZE[1]}" width="{NEW_SIZE[0]}" height="{NEW_SIZE[1]}">
  <!-- Icon-only marker (no gyro outline) - 3x larger -->
  
{new_drop_shadow}{centered_content}
{closing_tag}'''
    
    return svg_content

def process_markers():
    """Process all marker SVG files."""
    
    marker_files = sorted(MARKER_DIR.glob('marker-*.svg'))
    
    if not marker_files:
        print(f"❌ No marker-*.svg files found in {MARKER_DIR}")
        return
    
    print(f"🔍 Found {len(marker_files)} marker files")
    print(f"📂 Input directory: {MARKER_DIR}")
    print(f"📏 Output size: {NEW_SIZE[0]}x{NEW_SIZE[1]}px (3x scale)")
    print()
    
    processed = 0
    
    for marker_file in marker_files:
        try:
            # Read original marker SVG
            with open(marker_file, 'r', encoding='utf-8') as f:
                svg_content = f.read()
            
            # Scale to 3x and remove gyro outline
            scaled_svg = scale_svg_3x(svg_content)
            
            # Save back to same location (overwrite)
            with open(marker_file, 'w', encoding='utf-8') as f:
                f.write(scaled_svg)
            
            processed += 1
            print(f"✅ {marker_file.name}")
        
        except Exception as e:
            print(f"❌ Error processing {marker_file.name}: {e}")
    
    print()
    print(f"✨ Processed {processed} markers")
    print()
    print("🎯 Next steps:")
    print("   1. Update map.js to use new marker size (96x96)")
    print("   2. Regenerate site: python3 src/event_manager.py generate")

if __name__ == '__main__':
    print("=" * 60)
    print("🎨 Icon-Only Marker Generator")
    print("=" * 60)
    print()
    
    process_markers()
