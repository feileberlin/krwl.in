"""
Jsonplate Helper Module - KISS JSON Templating

Simple JSON templating using jsonplate library.
Replaces complex dict building and f-string interpolation with 
declarative JSON templates.

Features:
- Load templates from assets/json/templates/
- Parse templates with variable substitution
- Compile templates for reuse
- Validate template syntax

Usage:
    from jsonplate_helper import JsonTemplateHelper
    
    helper = JsonTemplateHelper(base_path)
    result = helper.render('runtime_config', debug=True, environment='development')
"""

import json
import logging
from pathlib import Path
from typing import Any, Dict, Optional

logger = logging.getLogger(__name__)

# Try to import jsonplate, fallback gracefully if not installed
try:
    import jsonplate
    JSONPLATE_AVAILABLE = True
except ImportError:
    JSONPLATE_AVAILABLE = False
    logger.warning("jsonplate not installed, using fallback json.loads")


class JsonTemplateHelper:
    """
    Helper class for JSON templating using jsonplate.
    
    Follows KISS principles:
    - Simple template loading from files
    - Direct variable substitution
    - No complex logic in templates (jsonplate doesn't support it anyway)
    """
    
    def __init__(self, base_path: Path):
        """
        Initialize JsonTemplateHelper.
        
        Args:
            base_path: Base path of the repository
        """
        self.base_path = Path(base_path)
        self.templates_dir = self.base_path / 'assets' / 'json' / 'templates'
        self._template_cache: Dict[str, str] = {}
    
    def load_template(self, template_name: str) -> str:
        """
        Load a template file from the templates directory.
        
        Args:
            template_name: Template filename (without .json extension)
            
        Returns:
            Template string content
            
        Raises:
            FileNotFoundError: If template file doesn't exist
        """
        if template_name in self._template_cache:
            return self._template_cache[template_name]
        
        template_path = self.templates_dir / f'{template_name}.json'
        if not template_path.exists():
            raise FileNotFoundError(f"Template not found: {template_path}")
        
        template_content = template_path.read_text(encoding='utf-8')
        self._template_cache[template_name] = template_content
        return template_content
    
    def render(self, template_name: str, **kwargs) -> Dict[str, Any]:
        """
        Render a template with the given parameters.
        
        Uses jsonplate for parameter substitution.
        Falls back to simple string replacement if jsonplate not available.
        
        Args:
            template_name: Name of the template file (without .json extension)
            **kwargs: Variables to substitute in the template
            
        Returns:
            Parsed JSON as a Python dict
            
        Example:
            result = helper.render('runtime_config', 
                debug=True, 
                environment='development')
        """
        template = self.load_template(template_name)
        
        if JSONPLATE_AVAILABLE:
            try:
                return jsonplate.parse(template, **kwargs)
            except Exception as e:
                logger.error(f"jsonplate parse error for '{template_name}': {e}")
                raise
        else:
            # Fallback: simple string replacement for {{var}} patterns
            return self._fallback_render(template, kwargs)
    
    def render_string(self, template_string: str, **kwargs) -> Dict[str, Any]:
        """
        Render a template string directly (without loading from file).
        
        Useful for inline templates that don't need to be stored in files.
        
        Args:
            template_string: JSON template string with {{placeholders}}
            **kwargs: Variables to substitute
            
        Returns:
            Parsed JSON as a Python dict
        """
        if JSONPLATE_AVAILABLE:
            try:
                return jsonplate.parse(template_string, **kwargs)
            except Exception as e:
                logger.error(f"jsonplate parse error: {e}")
                raise
        else:
            return self._fallback_render(template_string, kwargs)
    
    def _fallback_render(self, template: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Fallback renderer when jsonplate is not available.
        
        Simple string replacement for {{variable}} patterns,
        then JSON parsing.
        
        Args:
            template: Template string
            params: Dictionary of parameters
            
        Returns:
            Parsed JSON dict
        """
        import re
        
        # Replace {{variable}} patterns with JSON-encoded values
        def replace_match(match):
            var_name = match.group(1)
            if var_name in params:
                value = params[var_name]
                if isinstance(value, str):
                    return f'"{value}"'
                elif isinstance(value, bool):
                    return 'true' if value else 'false'
                elif value is None:
                    return 'null'
                else:
                    return json.dumps(value)
            return match.group(0)  # Keep original if not found
        
        # Also handle bare variable names (jsonplate syntax)
        result = template
        for key, value in params.items():
            # Replace bare variable names (not in quotes, not in strings)
            # This is a simplified approach
            if isinstance(value, bool):
                result = re.sub(rf'\b{key}\b(?!["\'])', 
                               'true' if value else 'false', 
                               result)
            elif isinstance(value, (int, float)):
                result = re.sub(rf'\b{key}\b(?!["\'])', str(value), result)
        
        # Replace {{variable}} patterns
        result = re.sub(r'\{\{(\w+)\}\}', replace_match, result)
        
        return json.loads(result)
    
    def validate_template(self, template_name: str) -> bool:
        """
        Validate that a template has correct JSON syntax.
        
        Args:
            template_name: Name of the template to validate
            
        Returns:
            True if valid, raises exception if invalid
        """
        template = self.load_template(template_name)
        
        # Try to parse with dummy values to check structure
        # Extract all variable names from the template
        import re
        variables = set(re.findall(r'\{\{(\w+)\}\}', template))
        variables.update(re.findall(r'\b([a-z_][a-z0-9_]*)\b', template))
        
        # Remove JSON keywords
        json_keywords = {'true', 'false', 'null'}
        variables -= json_keywords
        
        # Create dummy params
        dummy_params = {var: f"__{var}__" for var in variables}
        
        try:
            if JSONPLATE_AVAILABLE:
                jsonplate.parse(template, **dummy_params)
            else:
                self._fallback_render(template, dummy_params)
            return True
        except Exception as e:
            logger.error(f"Template validation failed for '{template_name}': {e}")
            raise
    
    def list_templates(self) -> list:
        """
        List all available templates.
        
        Returns:
            List of template names (without .json extension)
        """
        if not self.templates_dir.exists():
            return []
        
        return [f.stem for f in self.templates_dir.glob('*.json')]
    
    def clear_cache(self):
        """Clear the template cache."""
        self._template_cache.clear()


def is_jsonplate_available() -> bool:
    """Check if jsonplate library is available."""
    return JSONPLATE_AVAILABLE


# Convenience function for one-off template rendering
def render_json_template(template_string: str, **kwargs) -> Dict[str, Any]:
    """
    Render a JSON template string with parameters.
    
    Convenience function that doesn't require instantiating the helper.
    
    Args:
        template_string: JSON template with {{placeholders}} or bare variables
        **kwargs: Variables to substitute
        
    Returns:
        Parsed JSON as dict
        
    Example:
        result = render_json_template('''
        {
            "name": "{{app_name}}",
            "version": version_number,
            "debug": is_debug
        }
        ''', app_name="MyApp", version_number=1, is_debug=True)
    """
    if JSONPLATE_AVAILABLE:
        return jsonplate.parse(template_string, **kwargs)
    else:
        # Use fallback
        helper = JsonTemplateHelper(Path('.'))
        return helper._fallback_render(template_string, kwargs)


if __name__ == '__main__':
    # CLI for testing templates
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python jsonplate_helper.py <command> [args]")
        print("Commands:")
        print("  check       - Check if jsonplate is available")
        print("  list        - List available templates")
        print("  validate    - Validate a template")
        print("  test        - Run basic test")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == 'check':
        if JSONPLATE_AVAILABLE:
            print("✅ jsonplate is available")
        else:
            print("❌ jsonplate is NOT available (using fallback)")
        sys.exit(0)
    
    elif command == 'list':
        base_path = Path(__file__).parent.parent.parent
        helper = JsonTemplateHelper(base_path)
        templates = helper.list_templates()
        if templates:
            print(f"Available templates ({len(templates)}):")
            for t in templates:
                print(f"  - {t}")
        else:
            print("No templates found in assets/json/templates/")
    
    elif command == 'validate' and len(sys.argv) > 2:
        template_name = sys.argv[2]
        base_path = Path(__file__).parent.parent.parent
        helper = JsonTemplateHelper(base_path)
        try:
            helper.validate_template(template_name)
            print(f"✅ Template '{template_name}' is valid")
        except Exception as e:
            print(f"❌ Template '{template_name}' is invalid: {e}")
            sys.exit(1)
    
    elif command == 'test':
        # Basic functionality test
        result = render_json_template('''
        {
            "app": "{{app_name}}",
            "count": event_count,
            "debug": is_debug
        }
        ''', app_name="Test App", event_count=42, is_debug=True)
        
        print("Test result:")
        print(json.dumps(result, indent=2))
        assert result['app'] == 'Test App'
        assert result['count'] == 42
        assert result['debug'] is True
        print("✅ All tests passed")
    
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)
