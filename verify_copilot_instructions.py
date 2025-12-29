#!/usr/bin/env python3
"""
Verify that .github/copilot-instructions.md is up to date with the repository structure.

This script checks:
- File paths referenced in the instructions exist
- Module references are correct
- Test commands are valid
- Documentation references are accurate
- Configuration files match descriptions
"""

import os
import json
import re
from pathlib import Path
from typing import List, Tuple, Dict

# Colors for output
RED = '\033[91m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'

class CopilotInstructionsVerifier:
    def __init__(self, repo_root: Path):
        self.repo_root = repo_root
        self.instructions_path = repo_root / ".github" / "copilot-instructions.md"
        self.errors = []
        self.warnings = []
        self.successes = []
        
    def read_instructions(self) -> str:
        """Read the copilot instructions file."""
        if not self.instructions_path.exists():
            raise FileNotFoundError(f"Instructions file not found: {self.instructions_path}")
        return self.instructions_path.read_text()
    
    def check_file_references(self, instructions: str) -> None:
        """Check all file paths mentioned in the instructions exist."""
        print(f"\n{BLUE}Checking file references...{RESET}")
        
        # Extract file paths from markdown code blocks and inline code
        # Look for patterns like `path/to/file.ext`
        file_patterns = [
            r'`([a-zA-Z0-9_\-/\.]+\.(py|js|json|html|css|md|txt|sh|yml|yaml))`',
            r'- `([^`]+)` -',  # List items with files
            r'See `([^`]+)` for',  # References
            r'Edit `([^`]+)`',  # Edit instructions
            r'Check `([^`]+)`',  # Check instructions
        ]
        
        checked_files = set()
        for pattern in file_patterns:
            matches = re.findall(pattern, instructions)
            for match in matches:
                # Handle tuples from patterns with groups
                filepath = match[0] if isinstance(match, tuple) else match
                
                if filepath in checked_files:
                    continue
                checked_files.add(filepath)
                
                # Skip URLs and placeholders
                if filepath.startswith('http') or '{' in filepath or '...' in filepath or filepath == 'config.json':
                    continue
                
                full_path = self.repo_root / filepath
                if full_path.exists():
                    self.successes.append(f"✓ File exists: {filepath}")
                else:
                    # Check if it's in docs/ instead
                    alt_path = self.repo_root / "docs" / Path(filepath).name
                    if alt_path.exists() and not filepath.startswith('docs/'):
                        self.errors.append(
                            f"✗ File path incorrect: Instructions say `{filepath}` but file is at `docs/{Path(filepath).name}`"
                        )
                    else:
                        self.warnings.append(f"⚠ File not found: {filepath}")
    
    def check_module_references(self, instructions: str) -> None:
        """Check that referenced Python modules exist."""
        print(f"\n{BLUE}Checking module references...{RESET}")
        
        # Expected modules mentioned in instructions
        expected_modules = [
            'src/main.py',
            'src/modules/scraper.py',
            'src/modules/editor.py',
            'src/modules/generator.py',
            'src/modules/filter_tester.py',
            'src/modules/feature_verifier.py',
            'src/modules/scheduler.py',
            'src/modules/workflow_launcher.py',
            'src/modules/config_editor.py',
            'src/modules/kiss_checker.py',
            'src/modules/utils.py',
        ]
        
        for module_path in expected_modules:
            full_path = self.repo_root / module_path
            if full_path.exists():
                self.successes.append(f"✓ Module exists: {module_path}")
            else:
                self.errors.append(f"✗ Module missing: {module_path}")
        
        # Check for modules that exist but aren't mentioned
        modules_dir = self.repo_root / "src" / "modules"
        if modules_dir.exists():
            actual_modules = [f.name for f in modules_dir.glob("*.py") if f.name != "__init__.py"]
            mentioned_modules = [Path(m).name for m in expected_modules if m.startswith('src/modules/')]
            
            for actual in actual_modules:
                if actual not in mentioned_modules:
                    self.warnings.append(f"⚠ Module exists but not in instructions: src/modules/{actual}")
    
    def check_test_files(self, instructions: str) -> None:
        """Check that test files mentioned exist."""
        print(f"\n{BLUE}Checking test files...{RESET}")
        
        # Extract test commands from instructions
        test_patterns = [
            r'python3?\s+([a-zA-Z0-9_\-/\.]+\.py)',
            r'\./([a-zA-Z0-9_\-/\.]+\.sh)',
        ]
        
        checked = set()
        for pattern in test_patterns:
            matches = re.findall(pattern, instructions)
            for filepath in matches:
                if filepath in checked:
                    continue
                checked.add(filepath)
                
                full_path = self.repo_root / filepath
                if full_path.exists():
                    self.successes.append(f"✓ Test/script exists: {filepath}")
                else:
                    self.errors.append(f"✗ Test/script missing: {filepath}")
    
    def check_config_files(self, instructions: str) -> None:
        """Check configuration files mentioned."""
        print(f"\n{BLUE}Checking configuration files...{RESET}")
        
        expected_configs = [
            'config.prod.json',
            'config.dev.json',
            'config.preview.json',
            'static/config.json',
            'features.json',
            'requirements.txt',
        ]
        
        for config in expected_configs:
            full_path = self.repo_root / config
            if full_path.exists():
                self.successes.append(f"✓ Config exists: {config}")
            else:
                self.errors.append(f"✗ Config missing: {config}")
    
    def check_static_structure(self, instructions: str) -> None:
        """Check static/ directory structure."""
        print(f"\n{BLUE}Checking static/ directory structure...{RESET}")
        
        expected_files = [
            'static/index.html',
            'static/js/app.js',
            'static/css/style.css',
            'static/js/i18n.js',
            'static/content.json',
            'static/content.de.json',
            'static/.copilot-protected',
            'static/DO_NOT_EDIT_README.txt',
        ]
        
        for filepath in expected_files:
            full_path = self.repo_root / filepath
            if full_path.exists():
                self.successes.append(f"✓ Static file exists: {filepath}")
            else:
                self.errors.append(f"✗ Static file missing: {filepath}")
    
    def check_documentation_references(self, instructions: str) -> None:
        """Check documentation file references."""
        print(f"\n{BLUE}Checking documentation references...{RESET}")
        
        # Find all documentation references in the instructions
        doc_patterns = [
            r'Check `([^`]+\.md)`',
            r'See `([^`]+\.md)`',
            r'\[.*?\]\(([^)]+\.md)\)',
        ]
        
        checked = set()
        for pattern in doc_patterns:
            matches = re.findall(pattern, instructions)
            for filepath in matches:
                if filepath in checked:
                    continue
                checked.add(filepath)
                
                # Try the path as-is first
                full_path = self.repo_root / filepath
                if full_path.exists():
                    self.successes.append(f"✓ Documentation exists: {filepath}")
                else:
                    # Check if it's in docs/ directory
                    filename = Path(filepath).name
                    alt_path = self.repo_root / "docs" / filename
                    if alt_path.exists():
                        self.errors.append(
                            f"✗ Documentation path incorrect: Instructions say `{filepath}` but file is at `docs/{filename}`"
                        )
                    else:
                        self.warnings.append(f"⚠ Documentation not found: {filepath}")
    
    def verify_requirements(self) -> None:
        """Verify requirements.txt matches instructions."""
        print(f"\n{BLUE}Checking requirements.txt...{RESET}")
        
        req_path = self.repo_root / "requirements.txt"
        if not req_path.exists():
            self.errors.append("✗ requirements.txt not found")
            return
        
        requirements = req_path.read_text()
        
        # Check for packages mentioned in instructions
        expected_packages = [
            'requests>=2.31.0',
            'beautifulsoup4>=4.12.0',
            'lxml>=4.9.0',
            'feedparser>=6.0.10',
        ]
        
        for package in expected_packages:
            if package.split('>=')[0] in requirements:
                self.successes.append(f"✓ Package mentioned: {package.split('>=')[0]}")
            else:
                self.errors.append(f"✗ Package not in requirements.txt: {package}")
    
    def print_report(self) -> bool:
        """Print verification report and return success status."""
        print(f"\n{'='*80}")
        print(f"{BLUE}COPILOT INSTRUCTIONS VERIFICATION REPORT{RESET}")
        print(f"{'='*80}\n")
        
        if self.errors:
            print(f"{RED}ERRORS ({len(self.errors)}):{RESET}")
            for error in self.errors:
                print(f"  {error}")
            print()
        
        if self.warnings:
            print(f"{YELLOW}WARNINGS ({len(self.warnings)}):{RESET}")
            for warning in self.warnings:
                print(f"  {warning}")
            print()
        
        if self.successes and os.getenv('VERBOSE'):
            print(f"{GREEN}SUCCESSES ({len(self.successes)}):{RESET}")
            for success in self.successes:
                print(f"  {success}")
            print()
        
        # Summary
        print(f"{'='*80}")
        print(f"Summary: {len(self.errors)} errors, {len(self.warnings)} warnings, {len(self.successes)} checks passed")
        print(f"{'='*80}\n")
        
        if self.errors:
            print(f"{RED}❌ Verification FAILED - Please update .github/copilot-instructions.md{RESET}")
            return False
        elif self.warnings:
            print(f"{YELLOW}⚠️  Verification passed with warnings{RESET}")
            return True
        else:
            print(f"{GREEN}✅ All checks passed!{RESET}")
            return True
    
    def run(self) -> bool:
        """Run all verification checks."""
        instructions = self.read_instructions()
        
        self.check_file_references(instructions)
        self.check_module_references(instructions)
        self.check_test_files(instructions)
        self.check_config_files(instructions)
        self.check_static_structure(instructions)
        self.check_documentation_references(instructions)
        self.verify_requirements()
        
        return self.print_report()


def main():
    import sys
    
    # Enable verbose mode if --verbose flag is passed
    if '--verbose' in sys.argv:
        os.environ['VERBOSE'] = '1'
    
    repo_root = Path(__file__).parent
    verifier = CopilotInstructionsVerifier(repo_root)
    
    try:
        success = verifier.run()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"{RED}Error during verification: {e}{RESET}")
        sys.exit(1)


if __name__ == '__main__':
    main()
