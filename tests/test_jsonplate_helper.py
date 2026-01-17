"""
Test suite for jsonplate helper module.

Tests the JSON templating functionality using jsonplate library.
"""

import json
import sys
import unittest
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from modules.jsonplate_helper import (
    JsonTemplateHelper,
    render_json_template,
    is_jsonplate_available
)


class TestJsonplateHelper(unittest.TestCase):
    """Test cases for JsonTemplateHelper class."""
    
    @classmethod
    def setUpClass(cls):
        """Set up test fixtures."""
        cls.base_path = Path(__file__).parent.parent
        cls.helper = JsonTemplateHelper(cls.base_path)
    
    def test_jsonplate_available(self):
        """Test that jsonplate library is available."""
        # jsonplate should be installed
        self.assertTrue(is_jsonplate_available())
    
    def test_list_templates(self):
        """Test listing available templates."""
        templates = self.helper.list_templates()
        
        # Should have our core templates
        self.assertIn('runtime_config_base', templates)
        self.assertIn('time_filters', templates)
        self.assertIn('weather_config', templates)
    
    def test_render_runtime_config_base(self):
        """Test rendering runtime_config_base template."""
        result = self.helper.render(
            'runtime_config_base',
            debug_enabled=True,
            environment='development',
            map_config={'zoom': 13},
            data_source='both',
            data_sources={'real': {}, 'demo': {}}
        )
        
        # Check structure
        self.assertIn('debug', result)
        self.assertIn('app', result)
        self.assertIn('map', result)
        self.assertIn('data', result)
        
        # Check values
        self.assertTrue(result['debug'])
        self.assertEqual(result['app']['environment'], 'development')
        self.assertEqual(result['data']['source'], 'both')
    
    def test_render_time_filters(self):
        """Test rendering time_filters template."""
        result = self.helper.render(
            'time_filters',
            days_until_full_moon=15,
            full_moon_enabled=True,
            days_until_sunday=3,
            sunday_date_iso='2026-01-18',
            sunday_date_formatted='January 18',
            sunday_enabled=True
        )
        
        # Check structure
        self.assertIn('full_moon', result)
        self.assertIn('sunday', result)
        
        # Check values
        self.assertEqual(result['full_moon']['days_until'], 15)
        self.assertTrue(result['full_moon']['enabled'])
        self.assertEqual(result['sunday']['date_iso'], '2026-01-18')
    
    def test_render_weather_config(self):
        """Test rendering weather_config template."""
        weather_data = {'temperature': '15°C', 'dresscode': 'Light jacket'}
        
        result = self.helper.render(
            'weather_config',
            weather_enabled=True,
            display_config={'show_in_filter_bar': True},
            weather_data=weather_data
        )
        
        # Check structure
        self.assertIn('enabled', result)
        self.assertIn('display', result)
        self.assertIn('data', result)
        
        # Check values
        self.assertTrue(result['enabled'])
        self.assertEqual(result['data']['temperature'], '15°C')
    
    def test_render_string_simple(self):
        """Test rendering a simple inline template."""
        template = '{"name": "{{app_name}}", "count": event_count}'
        
        result = self.helper.render_string(
            template,
            app_name='Test App',
            event_count=42
        )
        
        self.assertEqual(result['name'], 'Test App')
        self.assertEqual(result['count'], 42)
    
    def test_render_string_boolean(self):
        """Test rendering template with boolean values."""
        template = '{"enabled": is_enabled, "disabled": is_disabled}'
        
        result = self.helper.render_string(
            template,
            is_enabled=True,
            is_disabled=False
        )
        
        self.assertTrue(result['enabled'])
        self.assertFalse(result['disabled'])
    
    def test_render_string_nested(self):
        """Test rendering template with nested objects."""
        template = '{"outer": {"inner": inner_value}}'
        
        result = self.helper.render_string(
            template,
            inner_value={'key': 'value'}
        )
        
        self.assertEqual(result['outer']['inner']['key'], 'value')
    
    def test_cache_clearing(self):
        """Test template cache clearing functionality."""
        # Load a template to populate cache
        template1 = self.helper.load_template('runtime_config_base')
        self.assertIsNotNone(template1)
        
        # Load again - should be cached (same result)
        template2 = self.helper.load_template('runtime_config_base')
        self.assertEqual(template1, template2)
        
        # Clear cache
        self.helper.clear_cache()
        
        # Load again - should work (cache cleared, reloads from file)
        template3 = self.helper.load_template('runtime_config_base')
        self.assertEqual(template1, template3)
    
    def test_template_not_found(self):
        """Test error handling for missing templates."""
        with self.assertRaises(FileNotFoundError):
            self.helper.load_template('nonexistent_template')


class TestRenderJsonTemplateFunction(unittest.TestCase):
    """Test cases for render_json_template convenience function."""
    
    def test_simple_template(self):
        """Test simple template rendering."""
        result = render_json_template(
            '{"key": "{{value}}"}',
            value='test'
        )
        
        self.assertEqual(result['key'], 'test')
    
    def test_numeric_values(self):
        """Test template with numeric values."""
        result = render_json_template(
            '{"count": num, "ratio": ratio_val}',
            num=42,
            ratio_val=3.14
        )
        
        self.assertEqual(result['count'], 42)
        self.assertAlmostEqual(result['ratio'], 3.14)
    
    def test_null_value(self):
        """Test template with null value passed as object."""
        # jsonplate handles null via object values, not bare null keyword
        result = render_json_template(
            '{"data": data_value}',
            data_value=None
        )
        
        self.assertIsNone(result['data'])


class TestSiteGeneratorIntegration(unittest.TestCase):
    """Integration tests with SiteGenerator."""
    
    @classmethod
    def setUpClass(cls):
        """Set up test fixtures."""
        cls.base_path = Path(__file__).parent.parent
        sys.path.insert(0, str(cls.base_path / 'src'))
    
    def test_site_generator_jsonplate_method(self):
        """Test SiteGenerator.build_runtime_config_with_jsonplate method."""
        from modules.site_generator import SiteGenerator
        
        gen = SiteGenerator(self.base_path)
        
        # Test with minimal config
        primary_config = {
            'debug': True,
            'app': {'environment': 'test'},
            'map': {'zoom': 13},
            'data': {'source': 'demo', 'sources': {}},
            'weather': {'enabled': False}
        }
        
        result = gen.build_runtime_config_with_jsonplate(primary_config, None)
        
        # Verify basic structure
        self.assertIn('debug', result)
        self.assertIn('app', result)
        self.assertIn('map', result)
        self.assertIn('data', result)
        self.assertIn('weather', result)
        self.assertIn('time_filters', result)
        
        # Verify values
        self.assertTrue(result['debug'])
        self.assertEqual(result['app']['environment'], 'test')
        self.assertEqual(result['data']['source'], 'demo')
        self.assertFalse(result['weather']['enabled'])
    
    def test_site_generator_with_weather(self):
        """Test SiteGenerator with weather enabled."""
        from modules.site_generator import SiteGenerator
        
        gen = SiteGenerator(self.base_path)
        
        primary_config = {
            'debug': False,
            'app': {'environment': 'production'},
            'map': {},
            'data': {'source': 'real', 'sources': {}},
            'weather': {
                'enabled': True,
                'display': {'show_in_filter_bar': True}
            }
        }
        
        weather_cache = {
            'hof': {
                'data': {
                    'temperature': '10°C',
                    'dresscode': 'Warm jacket'
                }
            }
        }
        
        result = gen.build_runtime_config_with_jsonplate(primary_config, weather_cache)
        
        # Verify weather is properly populated
        self.assertTrue(result['weather']['enabled'])
        self.assertEqual(result['weather']['data']['dresscode'], 'Warm jacket')


if __name__ == '__main__':
    # Run tests with verbosity
    unittest.main(verbosity=2)
