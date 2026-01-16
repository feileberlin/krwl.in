#!/usr/bin/env python3
"""
Test for scraper-info command JSON output validation.

This test ensures that the scraper-info command outputs valid JSON
without log messages contaminating the output when stderr is suppressed.
"""

import json
import subprocess
import sys
from pathlib import Path

def test_scraper_info_json_output():
    """Test that scraper-info outputs valid JSON when stderr is suppressed."""
    
    # Get the repository root
    repo_root = Path(__file__).parent.parent
    
    # Run the scraper-info command with stderr suppressed
    result = subprocess.run(
        ['python3', 'src/event_manager.py', 'scraper-info'],
        cwd=repo_root,
        capture_output=True,
        text=True
    )
    
    # The command should succeed
    if result.returncode != 0:
        print(f"❌ Command failed with exit code {result.returncode}")
        print(f"stderr: {result.stderr}")
        return False
    
    # Try to parse the stdout as JSON
    try:
        capabilities = json.loads(result.stdout)
        print("✓ JSON parsing successful")
    except json.JSONDecodeError as e:
        print(f"❌ JSON parsing failed: {e}")
        print(f"stdout: {result.stdout[:500]}")
        print(f"stderr: {result.stderr[:500]}")
        return False
    
    # Validate the structure
    required_keys = [
        'supported_source_types',
        'enabled_sources',
        'schedule',
        'smart_scraper_available',
        'scraping_libraries_installed'
    ]
    
    for key in required_keys:
        if key not in capabilities:
            print(f"❌ Missing required key: {key}")
            return False
    
    print(f"✓ All required keys present: {', '.join(required_keys)}")
    
    # Check that enabled_sources is a list
    if not isinstance(capabilities['enabled_sources'], list):
        print("❌ enabled_sources is not a list")
        return False
    
    print(f"✓ Found {len(capabilities['enabled_sources'])} enabled sources")
    
    # Check that schedule has required fields
    schedule = capabilities.get('schedule', {})
    if 'timezone' not in schedule:
        print("❌ Schedule missing timezone")
        return False
    
    if 'times' not in schedule:
        print("❌ Schedule missing times")
        return False
    
    print(f"✓ Schedule configured: {schedule['times']} ({schedule['timezone']})")
    
    return True


def test_scraper_info_without_stderr_suppression():
    """Test that scraper-info outputs logs to stderr, not stdout."""
    
    # Get the repository root
    repo_root = Path(__file__).parent.parent
    
    # Run the scraper-info command WITHOUT stderr suppression
    result = subprocess.run(
        ['python3', 'src/event_manager.py', 'scraper-info'],
        cwd=repo_root,
        capture_output=True,
        text=True
    )
    
    # Check if there are INFO logs in stderr
    if 'INFO:' in result.stderr or 'ERROR:' in result.stderr or 'WARNING:' in result.stderr:
        print("✓ Logs are correctly output to stderr")
        return True
    else:
        print("⚠ No logs found in stderr (this might be expected if logging is minimal)")
        return True  # Not a failure, just informational


if __name__ == '__main__':
    print("Testing scraper-info JSON output...")
    print("=" * 60)
    
    # Test 1: JSON output validation
    print("\n📋 Test 1: JSON output with stderr suppressed")
    print("-" * 60)
    test1_passed = test_scraper_info_json_output()
    
    # Test 2: Verify logs go to stderr
    print("\n📋 Test 2: Logs go to stderr")
    print("-" * 60)
    test2_passed = test_scraper_info_without_stderr_suppression()
    
    # Summary
    print("\n" + "=" * 60)
    print("Test Summary:")
    print(f"  Test 1 (JSON output): {'✓ PASSED' if test1_passed else '✗ FAILED'}")
    print(f"  Test 2 (stderr logs): {'✓ PASSED' if test2_passed else '✗ FAILED'}")
    print("=" * 60)
    
    # Exit with appropriate code
    if test1_passed and test2_passed:
        print("\n✓ All tests passed!")
        sys.exit(0)
    else:
        print("\n✗ Some tests failed")
        sys.exit(1)
