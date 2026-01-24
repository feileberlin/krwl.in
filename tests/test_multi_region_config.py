#!/usr/bin/env python3
"""
Test Multi-Region Configuration

Tests the new multi-region configuration structure in config.json
to ensure all regions are properly defined with required fields.
"""

import json
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))


class TestMultiRegionConfig:
    """Test suite for multi-region configuration"""
    
    def __init__(self):
        self.base_path = Path(__file__).parent.parent
        self.config_path = self.base_path / "config.json"
        self.config = None
        self.errors = []
        self.warnings = []
    
    def load_config_file(self):
        """Load and parse config.json"""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                self.config = json.load(f)
            return True
        except json.JSONDecodeError as e:
            self.errors.append(f"Failed to parse config.json: {e}")
            return False
        except FileNotFoundError:
            self.errors.append(f"Config file not found: {self.config_path}")
            return False
    
    def test_regions_section_exists(self):
        """Test that regions section exists in config"""
        print("  Testing: Regions section exists...")
        if 'regions' not in self.config:
            self.errors.append("Missing 'regions' section in config.json")
            return False
        
        regions = self.config['regions']
        if not isinstance(regions, dict):
            self.errors.append("'regions' must be a dictionary")
            return False
        
        if len(regions) == 0:
            self.warnings.append("'regions' section is empty")
        
        print(f"    ✓ Found {len(regions)} regions")
        return True
    
    def test_default_region_exists(self):
        """Test that defaultRegion field exists"""
        print("  Testing: Default region field exists...")
        if 'defaultRegion' not in self.config:
            self.errors.append("Missing 'defaultRegion' field in config.json")
            return False
        
        default_region = self.config['defaultRegion']
        if not isinstance(default_region, str):
            self.errors.append("'defaultRegion' must be a string")
            return False
        
        # Check if default region exists in regions
        if 'regions' in self.config and default_region not in self.config['regions']:
            self.errors.append(f"Default region '{default_region}' not found in regions section")
            return False
        
        print(f"    ✓ Default region: {default_region}")
        return True
    
    def test_supported_languages_exists(self):
        """Test that supportedLanguages field exists"""
        print("  Testing: Supported languages field exists...")
        if 'supportedLanguages' not in self.config:
            self.errors.append("Missing 'supportedLanguages' field in config.json")
            return False
        
        languages = self.config['supportedLanguages']
        if not isinstance(languages, list):
            self.errors.append("'supportedLanguages' must be a list")
            return False
        
        if len(languages) == 0:
            self.warnings.append("'supportedLanguages' is empty")
        
        print(f"    ✓ Supported languages: {', '.join(languages)}")
        return True
    
    def test_region_required_fields(self):
        """Test that each region has all required fields"""
        print("  Testing: Region required fields...")
        
        if 'regions' not in self.config:
            return False
        
        required_fields = [
            'name', 'displayName', 'center', 'zoom', 
            'boundingBox', 'dataSource', 'defaultLanguage', 'customFilters'
        ]
        
        regions = self.config['regions']
        all_valid = True
        
        for region_id, region_config in regions.items():
            print(f"    Checking region: {region_id}")
            
            for field in required_fields:
                if field not in region_config:
                    self.errors.append(f"Region '{region_id}' missing required field '{field}'")
                    all_valid = False
        
        if all_valid:
            print(f"    ✓ All {len(regions)} regions have required fields")
        
        return all_valid
    
    def test_region_center_coordinates(self):
        """Test that region centers have valid lat/lng coordinates"""
        print("  Testing: Region center coordinates...")
        
        if 'regions' not in self.config:
            return False
        
        regions = self.config['regions']
        all_valid = True
        
        for region_id, region_config in regions.items():
            if 'center' not in region_config:
                continue
            
            center = region_config['center']
            
            # Check structure
            if not isinstance(center, dict):
                self.errors.append(f"Region '{region_id}' center must be a dictionary")
                all_valid = False
                continue
            
            # Check required fields
            if 'lat' not in center or 'lng' not in center:
                self.errors.append(f"Region '{region_id}' center missing lat/lng")
                all_valid = False
                continue
            
            # Validate ranges
            lat = center['lat']
            lng = center['lng']
            
            if not isinstance(lat, (int, float)) or not isinstance(lng, (int, float)):
                self.errors.append(f"Region '{region_id}' center lat/lng must be numbers")
                all_valid = False
                continue
            
            if not (-90 <= lat <= 90):
                self.errors.append(f"Region '{region_id}' center lat {lat} out of range (-90 to 90)")
                all_valid = False
            
            if not (-180 <= lng <= 180):
                self.errors.append(f"Region '{region_id}' center lng {lng} out of range (-180 to 180)")
                all_valid = False
        
        if all_valid:
            print(f"    ✓ All region centers have valid coordinates")
        
        return all_valid
    
    def test_region_bounding_boxes(self):
        """Test that region bounding boxes are valid"""
        print("  Testing: Region bounding boxes...")
        
        if 'regions' not in self.config:
            return False
        
        regions = self.config['regions']
        all_valid = True
        
        for region_id, region_config in regions.items():
            if 'boundingBox' not in region_config:
                continue
            
            bbox = region_config['boundingBox']
            
            # Check structure
            if not isinstance(bbox, dict):
                self.errors.append(f"Region '{region_id}' boundingBox must be a dictionary")
                all_valid = False
                continue
            
            # Check required fields
            required = ['north', 'south', 'east', 'west']
            if not all(field in bbox for field in required):
                self.errors.append(f"Region '{region_id}' boundingBox missing required fields")
                all_valid = False
                continue
            
            # Validate ranges and logic
            north = bbox['north']
            south = bbox['south']
            east = bbox['east']
            west = bbox['west']
            
            if not all(isinstance(v, (int, float)) for v in [north, south, east, west]):
                self.errors.append(f"Region '{region_id}' boundingBox values must be numbers")
                all_valid = False
                continue
            
            if north <= south:
                self.errors.append(f"Region '{region_id}' boundingBox north must be > south")
                all_valid = False
            
            if east <= west:
                self.errors.append(f"Region '{region_id}' boundingBox east must be > west")
                all_valid = False
        
        if all_valid:
            print(f"    ✓ All region bounding boxes are valid")
        
        return all_valid
    
    def test_region_custom_filters(self):
        """Test that region custom filters are valid"""
        print("  Testing: Region custom filters...")
        
        if 'regions' not in self.config:
            return False
        
        regions = self.config['regions']
        all_valid = True
        
        for region_id, region_config in regions.items():
            if 'customFilters' not in region_config:
                continue
            
            filters = region_config['customFilters']
            
            if not isinstance(filters, list):
                self.errors.append(f"Region '{region_id}' customFilters must be a list")
                all_valid = False
                continue
            
            for i, filter_config in enumerate(filters):
                if not isinstance(filter_config, dict):
                    self.errors.append(f"Region '{region_id}' filter {i} must be a dictionary")
                    all_valid = False
                    continue
                
                # Check required fields
                required = ['id', 'name', 'center', 'radius', 'zoom']
                missing = [f for f in required if f not in filter_config]
                if missing:
                    self.errors.append(
                        f"Region '{region_id}' filter {i} missing: {', '.join(missing)}"
                    )
                    all_valid = False
                
                # Validate name is multilingual
                if 'name' in filter_config:
                    name = filter_config['name']
                    if not isinstance(name, dict):
                        self.errors.append(
                            f"Region '{region_id}' filter {i} name must be dictionary with language keys"
                        )
                        all_valid = False
                    elif 'de' not in name:
                        self.warnings.append(
                            f"Region '{region_id}' filter {i} missing German translation"
                        )
        
        if all_valid:
            print(f"    ✓ All region custom filters are valid")
        
        return all_valid
    
    def test_region_distance_presets(self):
        """Test that all regions have valid distance presets"""
        print("  Testing: Region distance presets...")
        
        if 'regions' not in self.config:
            return False
        
        regions = self.config['regions']
        all_valid = True
        
        for region_id, region_config in regions.items():
            # Check distancePresets exists
            if 'distancePresets' not in region_config:
                self.errors.append(f"Region '{region_id}' missing distancePresets")
                all_valid = False
                continue
            
            distance_presets = region_config['distancePresets']
            
            if not isinstance(distance_presets, list):
                self.errors.append(f"Region '{region_id}' distancePresets is not a list")
                all_valid = False
                continue
            
            if len(distance_presets) == 0:
                self.warnings.append(f"Region '{region_id}' has no distance presets")
            
            # Track preset IDs for uniqueness check
            preset_ids = set()
            
            for i, preset in enumerate(distance_presets):
                # Check required fields
                if 'id' not in preset:
                    self.errors.append(
                        f"Region '{region_id}' distance preset {i} missing id"
                    )
                    all_valid = False
                    continue
                
                preset_id = preset['id']
                
                # Check for duplicate IDs
                if preset_id in preset_ids:
                    self.errors.append(
                        f"Region '{region_id}' has duplicate distance preset ID: {preset_id}"
                    )
                    all_valid = False
                else:
                    preset_ids.add(preset_id)
                
                if 'name' not in preset:
                    self.errors.append(
                        f"Region '{region_id}' distance preset '{preset_id}' missing name"
                    )
                    all_valid = False
                elif not isinstance(preset['name'], dict):
                    self.errors.append(
                        f"Region '{region_id}' distance preset '{preset_id}' name is not a dict"
                    )
                    all_valid = False
                else:
                    # Check for language keys
                    if 'de' not in preset['name']:
                        self.errors.append(
                            f"Region '{region_id}' distance preset '{preset_id}' missing German name"
                        )
                        all_valid = False
                    if 'en' not in preset['name']:
                        self.errors.append(
                            f"Region '{region_id}' distance preset '{preset_id}' missing English name"
                        )
                        all_valid = False
                
                if 'distance_km' not in preset:
                    self.errors.append(
                        f"Region '{region_id}' distance preset '{preset_id}' missing distance_km"
                    )
                    all_valid = False
                elif not isinstance(preset['distance_km'], (int, float)) or preset['distance_km'] <= 0:
                    self.errors.append(
                        f"Region '{region_id}' distance preset '{preset_id}' distance_km must be a positive number"
                    )
                    all_valid = False
        
        if all_valid:
            print(f"    ✓ All region distance presets are valid")
        
        return all_valid
    
    def test_backward_compatibility(self):
        """Test that existing config fields still work"""
        print("  Testing: Backward compatibility...")
        
        # Check that old map config still exists
        if 'map' not in self.config:
            self.errors.append("Missing 'map' section (backward compatibility)")
            return False
        
        map_config = self.config['map']
        required_map_fields = ['default_center', 'default_zoom', 'tile_provider']
        
        for field in required_map_fields:
            if field not in map_config:
                self.errors.append(f"Missing map.{field} (backward compatibility)")
                return False
        
        print("    ✓ Old configuration structure preserved")
        return True
    
    def run_all_tests(self, verbose=False):
        """Run all tests and report results"""
        print("\n" + "="*60)
        print("Multi-Region Configuration Tests")
        print("="*60)
        
        # Load config
        print("\nLoading config.json...")
        if not self.load_config_file():
            self.print_results()
            return False
        
        print(f"  ✓ Config loaded successfully\n")
        
        # Run all tests
        tests = [
            self.test_backward_compatibility,
            self.test_regions_section_exists,
            self.test_default_region_exists,
            self.test_supported_languages_exists,
            self.test_region_required_fields,
            self.test_region_center_coordinates,
            self.test_region_bounding_boxes,
            self.test_region_custom_filters,
            self.test_region_distance_presets,
        ]
        
        passed = 0
        failed = 0
        
        for test in tests:
            try:
                if test():
                    passed += 1
                else:
                    failed += 1
            except Exception as e:
                self.errors.append(f"Test {test.__name__} raised exception: {e}")
                failed += 1
        
        # Print results
        self.print_results()
        
        return failed == 0
    
    def print_results(self):
        """Print test results"""
        print("\n" + "="*60)
        print("Test Results")
        print("="*60)
        
        if self.errors:
            print(f"\n❌ ERRORS ({len(self.errors)}):")
            for error in self.errors:
                print(f"  • {error}")
        
        if self.warnings:
            print(f"\n⚠️  WARNINGS ({len(self.warnings)}):")
            for warning in self.warnings:
                print(f"  • {warning}")
        
        if not self.errors and not self.warnings:
            print("\n✅ All tests passed!")
        elif not self.errors:
            print("\n✅ All tests passed (with warnings)")
        
        print()


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Test multi-region configuration')
    parser.add_argument('--verbose', action='store_true', help='Verbose output')
    args = parser.parse_args()
    
    tester = TestMultiRegionConfig()
    success = tester.run_all_tests(verbose=args.verbose)
    
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
