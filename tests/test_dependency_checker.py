#!/usr/bin/env python3
"""
Test Dependency Checker Module

Validates that dependency tracking works correctly.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.modules.dependency_checker import DependencyChecker


def test_dependency_checker():
    """Test basic dependency checker functionality"""
    print("Testing Dependency Checker...")
    
    # Initialize checker
    checker = DependencyChecker()
    
    # Test 1: Validate dependencies
    print("\n✓ Test 1: Validate dependencies")
    errors = checker.validate_dependencies()
    assert len(errors) == 0, f"Dependency validation errors: {errors}"
    print("  PASS: All dependencies are valid")
    
    # Test 2: Check for circular dependencies
    print("\n✓ Test 2: Check for circular dependencies")
    circular = checker.check_circular_dependencies()
    assert len(circular) == 0, f"Circular dependencies found: {circular}"
    print("  PASS: No circular dependencies")
    
    # Test 3: Calculate impact
    print("\n✓ Test 3: Calculate impact for interactive-map")
    impact = checker.calculate_impact('interactive-map')
    assert impact['feature_id'] == 'interactive-map'
    assert isinstance(impact['direct_dependents'], list)
    assert isinstance(impact['all_dependents'], list)
    assert impact['impact_score'] >= 0
    print(f"  PASS: Impact score = {impact['impact_score']}")
    
    # Test 4: Find dependents
    print("\n✓ Test 4: Find dependents")
    dependents = checker.find_dependents('interactive-map')
    assert isinstance(dependents, list)
    print(f"  PASS: Found {len(dependents)} direct dependents")
    
    # Test 5: Analyze JavaScript dependencies
    print("\n✓ Test 5: Analyze JavaScript dependencies")
    js_deps = checker.analyze_js_dependencies()
    assert 'app.js' in js_deps
    assert 'map.js' in js_deps
    print(f"  PASS: Analyzed {len(js_deps)} JavaScript files")
    
    # Test 6: Analyze Python dependencies
    print("\n✓ Test 6: Analyze Python dependencies")
    py_deps = checker.analyze_python_dependencies()
    assert len(py_deps) > 0
    print(f"  PASS: Analyzed {len(py_deps)} Python files")
    
    # Test 7: Feature lookup
    print("\n✓ Test 7: Feature lookup")
    feature = checker.get_feature_by_id('interactive-map')
    assert feature is not None
    assert feature['id'] == 'interactive-map'
    print("  PASS: Feature lookup works")
    
    print("\n" + "="*60)
    print("✅ All tests passed!")
    print("="*60)
    return True


if __name__ == '__main__':
    try:
        test_dependency_checker()
        sys.exit(0)
    except AssertionError as e:
        print(f"\n❌ Test failed: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
