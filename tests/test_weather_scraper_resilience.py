#!/usr/bin/env python3
"""Test weather scraper resilience and retry logic

This test verifies that the weather scraper handles network failures gracefully
with retry logic and proper fallback to cached data.
"""

import sys
import unittest
import json
import tempfile
import shutil
from pathlib import Path
from unittest.mock import patch, Mock
import requests

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from modules.weather_scraper import WeatherScraper
from modules.utils import load_config


class TestWeatherScraperResilience(unittest.TestCase):
    """Test weather scraper resilience to network failures"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.base_path = Path(__file__).parent.parent
        self.temp_dir = Path(tempfile.mkdtemp())
        
        # Create necessary directories
        self.test_assets_dir = self.temp_dir / 'assets' / 'json'
        self.test_assets_dir.mkdir(parents=True)
        
        # Create weather dresscodes file
        dresscodes = {
            "accepted_dresscodes": [
                "Light jacket",
                "Warm coat",
                "T-shirt",
                "Sweater"
            ]
        }
        dresscodes_file = self.test_assets_dir / 'weather_dresscodes.json'
        with open(dresscodes_file, 'w') as f:
            json.dump(dresscodes, f)
        
        # Create test config with retry settings
        self.test_config = {
            'weather': {
                'enabled': True,
                'cache_hours': 1,
                'timeout': 5,
                'max_retries': 3,
                'retry_delay_base': 0.1  # Fast retries for testing
            }
        }
    
    def tearDown(self):
        """Clean up test fixtures"""
        if self.temp_dir.exists():
            shutil.rmtree(self.temp_dir)
    
    def test_retry_on_timeout(self):
        """Test that scraper retries on timeout errors"""
        scraper = WeatherScraper(self.temp_dir, self.test_config)
        
        # Mock requests to timeout twice then succeed
        # Use realistic MSN Weather HTML structure
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.content = b'<html><div data-id="dressingIndex" aria-label="Dress for 10C: Light jacket recommended"></div></html>'
        
        call_count = [0]
        
        def mock_get(*args, **kwargs):
            call_count[0] += 1
            if call_count[0] <= 2:
                raise requests.exceptions.Timeout("Connection timeout")
            return mock_response
        
        with patch('requests.get', side_effect=mock_get):
            result = scraper._scrape_weather("Test City", 50.0, 11.0)
            
            # Should succeed on third attempt
            self.assertIsNotNone(result)
            self.assertIn('light jacket', result['dresscode'].lower())
            self.assertEqual(call_count[0], 3)
    
    def test_retry_on_connection_error(self):
        """Test that scraper retries on connection errors"""
        scraper = WeatherScraper(self.temp_dir, self.test_config)
        
        # Mock requests to fail with connection error
        with patch('requests.get', side_effect=requests.exceptions.ConnectionError("Connection refused")):
            result = scraper._scrape_weather("Test City", 50.0, 11.0)
            
            # Should fail after all retries exhausted
            self.assertIsNone(result)
    
    def test_fallback_to_cache_on_failure(self):
        """Test that scraper falls back to cache when fresh scraping fails"""
        scraper = WeatherScraper(self.temp_dir, self.test_config)
        
        # Create cache with valid, recent data (within cache window)
        # Use location_name as cache key to match how get_weather will look it up
        from datetime import datetime, timedelta
        recent_time = datetime.now() - timedelta(minutes=30)  # 30 mins ago, within 1 hour cache
        
        cache_data = {
            "location_Test City": {
                "timestamp": recent_time.isoformat(),
                "data": {
                    "dresscode": "Warm coat",
                    "temperature": "5°C",
                    "location": "Test City",
                    "timestamp": recent_time.isoformat()
                }
            }
        }
        cache_file = self.test_assets_dir / 'weather_cache.json'
        with open(cache_file, 'w') as f:
            json.dump(cache_data, f)
        
        # Mock requests to fail
        with patch('requests.get', side_effect=requests.exceptions.ConnectionError("Connection refused")):
            # Should return cached data
            result = scraper.get_weather("Test City", 50.0, 11.0)
            
            self.assertIsNotNone(result)
            self.assertEqual(result['dresscode'], 'Warm coat')
            self.assertEqual(result['temperature'], '5°C')
    
    def test_no_infinite_retry(self):
        """Test that scraper doesn't retry indefinitely"""
        scraper = WeatherScraper(self.temp_dir, self.test_config)
        
        call_count = [0]
        
        def mock_get(*args, **kwargs):
            call_count[0] += 1
            raise requests.exceptions.Timeout("Timeout")
        
        with patch('requests.get', side_effect=mock_get):
            result = scraper._scrape_weather("Test City", 50.0, 11.0)
            
            # Should fail after max_retries attempts
            self.assertIsNone(result)
            self.assertEqual(call_count[0], self.test_config['weather']['max_retries'])
    
    def test_http_error_handling(self):
        """Test that scraper handles HTTP errors properly"""
        scraper = WeatherScraper(self.temp_dir, self.test_config)
        
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("500 Server Error")
        
        with patch('requests.get', return_value=mock_response):
            result = scraper._scrape_weather("Test City", 50.0, 11.0)
            
            self.assertIsNone(result)
    
    def test_invalid_dresscode_retry(self):
        """Test that scraper retries when dresscode is invalid"""
        scraper = WeatherScraper(self.temp_dir, self.test_config)
        
        # Mock response with invalid dresscode first, then valid
        invalid_response = Mock()
        invalid_response.status_code = 200
        invalid_response.content = b'<html><div>No dresscode here</div></html>'
        
        valid_response = Mock()
        valid_response.status_code = 200
        valid_response.content = b'<html><div data-id="dressingIndex" aria-label="Dress for 10C: Light jacket recommended"></div></html>'
        
        call_count = [0]
        
        def mock_get(*args, **kwargs):
            call_count[0] += 1
            if call_count[0] == 1:
                return invalid_response
            return valid_response
        
        with patch('requests.get', side_effect=mock_get):
            result = scraper._scrape_weather("Test City", 50.0, 11.0)
            
            # Should succeed on second attempt
            self.assertIsNotNone(result)
            self.assertIn('light jacket', result['dresscode'].lower())


def run_tests(verbose=False):
    """Run all tests"""
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestWeatherScraperResilience)
    runner = unittest.TextTestRunner(verbosity=2 if verbose else 1)
    result = runner.run(suite)
    return result.wasSuccessful()


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Test weather scraper resilience')
    parser.add_argument('--verbose', action='store_true', help='Verbose output')
    args = parser.parse_args()
    
    success = run_tests(verbose=args.verbose)
    sys.exit(0 if success else 1)
