#!/usr/bin/env python3
"""
Tests for debug comments behavior in site generator.

This test validates that debug comments are correctly enabled/disabled based on:
1. Environment variable DEBUG_COMMENTS (highest priority)
2. Config file debug_comments.force_enabled setting
3. Config file environment forced to "development"
4. Automatic environment detection from OS (fallback)
"""

import json
import os
import sys
import tempfile
import shutil
from pathlib import Path

# Add src directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from modules.site_generator import SiteGenerator


def create_test_config(base_path, environment='auto', force_enabled=False):
    """Create a minimal test config.json file"""
    config = {
        "environment": environment,
        "debug_comments": {
            "force_enabled": force_enabled
        },
        "app": {
            "name": "Test App",
            "environment": "test",
            "repository": {
                "owner": "test",
                "name": "test",
                "url": "https://github.com/test/test"
            }
        },
        "data": {
            "sources": {
                "real": {"url": "events.json", "description": "Real events"},
                "demo": {"url": "events.demo.json", "description": "Demo events"},
                "both": {"urls": ["events.json", "events.demo.json"], "description": "Both"}
            }
        },
        "scraping": {
            "sources": [],
            "interval_minutes": 60
        },
        "filtering": {
            "max_distance_km": 5.0,
            "show_until": "next_sunrise"
        },
        "map": {
            "default_center": {"lat": 50.0, "lon": 11.0},
            "default_zoom": 13,
            "tile_provider": "https://example.com/{z}/{x}/{y}.png",
            "attribution": "Test"
        },
        "editor": {
            "require_approval": True,
            "auto_publish": False
        }
    }
    
    config_path = base_path / 'config.json'
    with open(config_path, 'w') as f:
        json.dump(config, f, indent=2)
    
    # Create required directories
    (base_path / 'assets' / 'json').mkdir(parents=True, exist_ok=True)
    
    return config_path


def test_debug_comments_forced_development():
    """Test that debug comments are enabled when environment is forced to 'development'"""
    print("\n" + "="*80)
    print("TEST: Debug comments with environment forced to 'development'")
    print("="*80)
    
    # Create temporary directory
    with tempfile.TemporaryDirectory() as tmpdir:
        base_path = Path(tmpdir)
        
        # Clear any environment variables that might interfere
        env_backup = os.environ.get('DEBUG_COMMENTS')
        if 'DEBUG_COMMENTS' in os.environ:
            del os.environ['DEBUG_COMMENTS']
        
        try:
            # Create config with environment forced to 'development'
            create_test_config(base_path, environment='development', force_enabled=False)
            
            # Initialize site generator
            generator = SiteGenerator(base_path)
            
            # Check that debug comments are enabled
            if generator.enable_debug_comments:
                print("✓ PASS: Debug comments are ENABLED (as expected)")
                return True
            else:
                print("✗ FAIL: Debug comments are DISABLED (should be ENABLED)")
                return False
        
        finally:
            # Restore environment variable
            if env_backup is not None:
                os.environ['DEBUG_COMMENTS'] = env_backup


def test_debug_comments_forced_production():
    """Test that debug comments are disabled when environment is forced to 'production'"""
    print("\n" + "="*80)
    print("TEST: Debug comments with environment forced to 'production'")
    print("="*80)
    
    # Create temporary directory
    with tempfile.TemporaryDirectory() as tmpdir:
        base_path = Path(tmpdir)
        
        # Clear any environment variables that might interfere
        env_backup = os.environ.get('DEBUG_COMMENTS')
        if 'DEBUG_COMMENTS' in os.environ:
            del os.environ['DEBUG_COMMENTS']
        
        try:
            # Create config with environment forced to 'production'
            create_test_config(base_path, environment='production', force_enabled=False)
            
            # Initialize site generator
            generator = SiteGenerator(base_path)
            
            # Check that debug comments are disabled
            if not generator.enable_debug_comments:
                print("✓ PASS: Debug comments are DISABLED (as expected)")
                return True
            else:
                print("✗ FAIL: Debug comments are ENABLED (should be DISABLED)")
                return False
        
        finally:
            # Restore environment variable
            if env_backup is not None:
                os.environ['DEBUG_COMMENTS'] = env_backup


def test_debug_comments_force_enabled_setting():
    """Test that debug_comments.force_enabled overrides environment"""
    print("\n" + "="*80)
    print("TEST: Debug comments with force_enabled=true (overrides production)")
    print("="*80)
    
    # Create temporary directory
    with tempfile.TemporaryDirectory() as tmpdir:
        base_path = Path(tmpdir)
        
        # Clear any environment variables that might interfere
        env_backup = os.environ.get('DEBUG_COMMENTS')
        if 'DEBUG_COMMENTS' in os.environ:
            del os.environ['DEBUG_COMMENTS']
        
        try:
            # Create config with production + force_enabled=true
            create_test_config(base_path, environment='production', force_enabled=True)
            
            # Initialize site generator
            generator = SiteGenerator(base_path)
            
            # Check that debug comments are enabled (force_enabled overrides)
            if generator.enable_debug_comments:
                print("✓ PASS: Debug comments are ENABLED (force_enabled overrides production)")
                return True
            else:
                print("✗ FAIL: Debug comments are DISABLED (force_enabled should override)")
                return False
        
        finally:
            # Restore environment variable
            if env_backup is not None:
                os.environ['DEBUG_COMMENTS'] = env_backup


def test_debug_comments_env_variable_override():
    """Test that DEBUG_COMMENTS environment variable has highest priority"""
    print("\n" + "="*80)
    print("TEST: Debug comments with DEBUG_COMMENTS=true env var (highest priority)")
    print("="*80)
    
    # Create temporary directory
    with tempfile.TemporaryDirectory() as tmpdir:
        base_path = Path(tmpdir)
        
        # Set environment variable
        env_backup = os.environ.get('DEBUG_COMMENTS')
        os.environ['DEBUG_COMMENTS'] = 'true'
        
        try:
            # Create config with production (should be overridden by env var)
            create_test_config(base_path, environment='production', force_enabled=False)
            
            # Initialize site generator
            generator = SiteGenerator(base_path)
            
            # Check that debug comments are enabled (env var overrides all)
            if generator.enable_debug_comments:
                print("✓ PASS: Debug comments are ENABLED (env var overrides all)")
                return True
            else:
                print("✗ FAIL: Debug comments are DISABLED (env var should override)")
                return False
        
        finally:
            # Restore environment variable
            if env_backup is not None:
                os.environ['DEBUG_COMMENTS'] = env_backup
            else:
                del os.environ['DEBUG_COMMENTS']


def main():
    """Run all tests"""
    print("\n" + "="*80)
    print("DEBUG COMMENTS TEST SUITE")
    print("="*80)
    
    tests = [
        test_debug_comments_forced_development,
        test_debug_comments_forced_production,
        test_debug_comments_force_enabled_setting,
        test_debug_comments_env_variable_override
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"✗ TEST EXCEPTION: {e}")
            import traceback
            traceback.print_exc()
            results.append(False)
    
    # Summary
    print("\n" + "="*80)
    print("TEST SUMMARY")
    print("="*80)
    passed = sum(results)
    total = len(results)
    print(f"Passed: {passed}/{total}")
    
    if passed == total:
        print("\n✓ ALL TESTS PASSED")
        return 0
    else:
        print(f"\n✗ {total - passed} TEST(S) FAILED")
        return 1


if __name__ == '__main__':
    sys.exit(main())
