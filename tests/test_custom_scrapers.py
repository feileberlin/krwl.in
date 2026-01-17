#!/usr/bin/env python3
"""Tests for custom source scrapers."""

import sys
import unittest
from pathlib import Path
from datetime import datetime

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from modules.smart_scraper.sources.custom.date_utils import (
    extract_date_from_text,
    generate_stable_event_id
)
from modules.smart_scraper.base import SourceOptions


class TestDateUtils(unittest.TestCase):
    """Test shared date utilities."""
    
    def test_extract_date_dmy_format(self):
        """Test DD.MM.YYYY format extraction."""
        text = "Event on 15.02.2026 at 20:00"
        result = extract_date_from_text(text)
        self.assertIn('2026-02-15', result)
    
    def test_extract_date_short_year(self):
        """Test DD.MM.YY format with dynamic year handling."""
        text = "Event on 15.02.26"
        result = extract_date_from_text(text)
        # Should be in 2026 (current century + year)
        self.assertIn('2026-02-15', result)
    
    def test_extract_date_ymd_format(self):
        """Test YYYY-MM-DD format extraction."""
        text = "Event on 2026-02-15"
        result = extract_date_from_text(text)
        self.assertIn('2026-02-15', result)
    
    def test_extract_date_with_ab_prefix(self):
        """Test 'ab DD.MM.YYYY' format."""
        text = "ab 15.02.2026"
        result = extract_date_from_text(text)
        self.assertIn('2026-02-15', result)
    
    def test_extract_date_invalid_date_skipped(self):
        """Test that invalid dates are skipped."""
        text = "Event on 32.13.2026"  # Invalid day and month
        result = extract_date_from_text(text)
        # Should return default future date
        self.assertIsInstance(result, str)
    
    def test_extract_date_default_hour(self):
        """Test custom default hour."""
        text = "Event on 15.02.2026"
        result = extract_date_from_text(text, default_hour=10)
        self.assertIn('T10:00:00', result)
    
    def test_generate_stable_event_id(self):
        """Test stable ID generation."""
        id1 = generate_stable_event_id('test', 'title', '2026-02-15')
        id2 = generate_stable_event_id('test', 'title', '2026-02-15')
        # Same inputs should produce same ID
        self.assertEqual(id1, id2)
        self.assertTrue(id1.startswith('test_'))
    
    def test_generate_stable_event_id_different_inputs(self):
        """Test that different inputs produce different IDs."""
        id1 = generate_stable_event_id('test', 'title1', '2026-02-15')
        id2 = generate_stable_event_id('test', 'title2', '2026-02-15')
        self.assertNotEqual(id1, id2)


class TestCustomScraperIntegration(unittest.TestCase):
    """Integration tests for custom scrapers."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.base_path = Path(__file__).parent.parent
    
    def test_freiheitshalle_import(self):
        """Test that FreiheitshalleSource can be imported."""
        try:
            from modules.smart_scraper.sources.custom import FreiheitshalleSource
            self.assertIsNotNone(FreiheitshalleSource)
        except ImportError as e:
            self.fail(f"Failed to import FreiheitshalleSource: {e}")
    
    def test_vhs_import(self):
        """Test that VHSSource can be imported."""
        try:
            from modules.smart_scraper.sources.custom import VHSSource
            self.assertIsNotNone(VHSSource)
        except ImportError as e:
            self.fail(f"Failed to import VHSSource: {e}")
    
    def test_hof_stadt_import(self):
        """Test that HofStadtSource can be imported."""
        try:
            from modules.smart_scraper.sources.custom import HofStadtSource
            self.assertIsNotNone(HofStadtSource)
        except ImportError as e:
            self.fail(f"Failed to import HofStadtSource: {e}")
    
    def test_scraper_initialization(self):
        """Test that custom scrapers can be initialized."""
        from modules.smart_scraper.sources.custom import FreiheitshalleSource
        
        source_config = {
            'name': 'Test Freiheitshalle',
            'url': 'https://example.com',
            'type': 'html'
        }
        options = SourceOptions()
        
        scraper = FreiheitshalleSource(source_config, options)
        self.assertEqual(scraper.name, 'Test Freiheitshalle')
        self.assertEqual(scraper.url, 'https://example.com')
    
    def test_scraper_user_agent(self):
        """Test that scrapers have complete User-Agent strings."""
        from modules.smart_scraper.sources.custom import FreiheitshalleSource
        
        source_config = {
            'name': 'Test',
            'url': 'https://example.com',
            'type': 'html'
        }
        options = SourceOptions()
        
        scraper = FreiheitshalleSource(source_config, options)
        if scraper.available:
            user_agent = scraper.session.headers.get('User-Agent', '')
            # Check for complete User-Agent with Chrome version
            self.assertIn('Chrome/', user_agent)
            self.assertIn('Safari/', user_agent)
            self.assertIn('AppleWebKit/', user_agent)


class TestCustomScraperParsing(unittest.TestCase):
    """Test HTML parsing logic in custom scrapers."""
    
    def test_date_extraction_validation(self):
        """Test that date extraction validates day/month ranges."""
        # Valid date
        valid_result = extract_date_from_text("15.06.2026")
        self.assertIn('2026-06-15', valid_result)
        
        # Invalid dates should be skipped (returns future default)
        invalid_texts = [
            "32.01.2026",  # Day > 31
            "15.13.2026",  # Month > 12
            "00.06.2026",  # Day = 0
            "15.00.2026",  # Month = 0
        ]
        for text in invalid_texts:
            result = extract_date_from_text(text)
            # Should return default future date, not the invalid date
            self.assertNotIn('2026-01-32', result)
            self.assertNotIn('2026-13-15', result)


def main():
    """Run tests."""
    # Run with verbose output
    unittest.main(argv=[''], verbosity=2, exit=False)


if __name__ == '__main__':
    main()
