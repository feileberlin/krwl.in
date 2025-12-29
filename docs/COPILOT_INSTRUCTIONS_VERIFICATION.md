# Copilot Instructions Verification

This document describes the automated verification system for `.github/copilot-instructions.md`.

## Purpose

The Copilot instructions file serves as the primary guide for GitHub Copilot and AI assistants working on this repository. It's critical that this file stays in sync with the actual repository structure, features, and documentation.

## Verification Script

The `verify_copilot_instructions.py` script automatically checks that the Copilot instructions are up to date.

### What It Checks

1. **File References** - All file paths mentioned in the instructions exist
2. **Module References** - All Python modules referenced are present
3. **Test Files** - All test scripts and commands are valid
4. **Configuration Files** - All config files mentioned exist
5. **Static Structure** - Frontend files in `static/` directory are correct
6. **Documentation References** - All documentation links point to real files
7. **Dependencies** - Required packages in `requirements.txt` match instructions

### Running the Verification

```bash
# Basic check
python3 verify_copilot_instructions.py

# Verbose output (shows all successes)
python3 verify_copilot_instructions.py --verbose
```

### Exit Codes

- `0` - All checks passed (or passed with warnings)
- `1` - One or more checks failed

## Output Format

The script provides a detailed report with three sections:

### Errors ❌

Critical issues that must be fixed:
- File paths that don't exist
- Incorrect documentation references
- Missing required files

### Warnings ⚠️

Non-critical issues for review:
- Files that exist but aren't mentioned
- Optional features not documented

### Successes ✅

All checks that passed (visible with `--verbose`):
- Correct file references
- Valid module paths
- Existing documentation

## Example Output

```
================================================================================
COPILOT INSTRUCTIONS VERIFICATION REPORT
================================================================================

ERRORS (3):
  ✗ File path incorrect: Instructions say `TESTING.md` but file is at `docs/TESTING.md`
  ✗ Documentation path incorrect: Instructions say `.github/FEATURE_REGISTRY.md` but file is at `docs/FEATURE_REGISTRY.md`
  ✗ Config missing: config.preview.json

WARNINGS (2):
  ⚠ Module exists but not in instructions: src/modules/utils.py
  ⚠ config.preview.json exists but not mentioned in instructions

SUCCESSES (75):
  ✓ File exists: requirements.txt
  ✓ Module exists: src/main.py
  ... (shown with --verbose flag)

================================================================================
Summary: 3 errors, 2 warnings, 75 checks passed
================================================================================

❌ Verification FAILED - Please update .github/copilot-instructions.md
```

## Common Fixes

### Incorrect File Paths

If you see errors about incorrect file paths, update the references in `.github/copilot-instructions.md`:

```markdown
# Before
- Check `TESTING.md` for comprehensive testing guide

# After
- Check `docs/TESTING.md` for comprehensive testing guide
```

### Missing Modules

If new modules are added to `src/modules/`, add them to the "Key Modules" section:

```markdown
- **Key Modules**:
  - `src/main.py` - TUI entry point
  - `src/modules/new_module.py` - Description of new module
```

### Missing Configuration Files

If a new config file is added (like `config.preview.json`), update the Configuration section:

```markdown
### Configuration
- `config.prod.json` - Production
- `config.dev.json` - Development
- `config.preview.json` - Preview environment
```

## Integration with CI/CD

This verification script should be run as part of the CI/CD pipeline to ensure the Copilot instructions stay up to date. It's included in the feature registry and can be triggered via:

```bash
python3 verify_features.py --verbose
```

Which will run this script along with all other feature verifications.

## When to Update

Update `.github/copilot-instructions.md` when:

1. **New files/modules are added** - Document their purpose and location
2. **File paths change** - Update all references
3. **New tests are created** - Add to the testing section
4. **Documentation is reorganized** - Fix all documentation links
5. **Configuration files change** - Update config section
6. **New features are added** - Document them appropriately

## Maintenance

The verification script itself should be maintained to:

1. Add new checks as the repository evolves
2. Update patterns to match new code structures
3. Refine error messages for clarity
4. Add more detailed validation logic

## Feature Registry Entry

This verification system is registered in `features.json`:

```json
{
    "id": "copilot-instructions-verification",
    "name": "Copilot Instructions Verification",
    "description": "Automated verification tool...",
    "category": "infrastructure",
    "files": [
        "verify_copilot_instructions.py",
        ".github/copilot-instructions.md"
    ],
    "test_command": "python3 verify_copilot_instructions.py --verbose"
}
```

## Related Documentation

- [Feature Registry](FEATURE_REGISTRY.md) - All features documentation
- [Testing Guide](TESTING.md) - How to test the codebase
- [Development Environment](DEV_ENVIRONMENT.md) - Setup guide

## Troubleshooting

### False Positives

If you get a warning about a generic reference (like `config.json` referring to the concept, not a specific file), you can add it to the skip list in the verification script:

```python
if filepath.startswith('http') or '{' in filepath or '...' in filepath or filepath == 'config.json':
    continue
```

### Script Not Finding Files

Ensure you're running the script from the repository root:

```bash
cd /path/to/krwl-hof
python3 verify_copilot_instructions.py
```

### Permission Denied

Make the script executable:

```bash
chmod +x verify_copilot_instructions.py
```

## Contributing

When contributing to the Copilot instructions or verification script:

1. Test your changes with `python3 verify_copilot_instructions.py --verbose`
2. Ensure all checks pass (0 errors)
3. Document any new checks you add
4. Update this documentation if verification logic changes
