# Markdown Linting - Quick Reference

## Overview

The KRWL HOF project now includes a built-in markdown linting tool to maintain
documentation quality and consistency across all markdown files.

## Features

✅ **Heading Structure**
- Checks for single H1 heading per file
- Validates heading hierarchy (no skipped levels)

✅ **Code Quality**
- Ensures fenced code blocks have language tags
- Warns about long lines (>120 characters for prose)

✅ **Formatting**
- Detects trailing whitespace
- Identifies excessive blank lines
- Ensures files end with newline

✅ **Auto-Fix**
- Automatically removes trailing whitespace
- Removes excessive blank lines
- Adds missing file-ending newline

## Usage

### Via CLI (Recommended)

```bash
# List all documentation tasks
python3 src/event_manager.py docs --list

# Lint all markdown files
python3 src/event_manager.py docs lint-markdown --all

# Lint specific file
python3 src/event_manager.py docs lint-markdown README.md

# Lint with auto-fix
python3 src/event_manager.py docs lint-markdown --all --fix

# Lint specific directory
python3 src/event_manager.py docs lint-markdown .github/

# Verbose output
python3 src/event_manager.py docs lint-markdown --all --verbose
```

### Direct Script Usage

```bash
# Lint all markdown files
python3 scripts/lint_markdown.py --all

# Lint specific file
python3 scripts/lint_markdown.py README.md

# Lint with auto-fix
python3 scripts/lint_markdown.py --all --fix

# Lint specific directory
python3 scripts/lint_markdown.py .github/

# Get help
python3 scripts/lint_markdown.py --help
```

## Example Output

```bash
$ python3 src/event_manager.py docs lint-markdown README.md

📝 README.md
----------------------------------------------------------------------
  ❌ ERROR: Line 40: Multiple H1 headings found (only one allowed)
  ⚠️  WARNING: Line 53: Code block without language tag (e.g., ```python)
  ⚠️  WARNING: Line 104: Trailing whitespace
  ⚠️  WARNING: Line 13: Line too long (256 > 120 characters)
```

## Error Types

### Errors (❌)
Issues that should be fixed:
- Multiple H1 headings
- Malformed headings (missing space after #)

### Warnings (⚠️)
Issues to consider:
- Skipped heading levels
- Long lines (>120 chars)
- Code blocks without language tags
- Trailing whitespace
- Multiple consecutive blank lines
- Missing file-ending newline

## Auto-Fix Capabilities

The `--fix` flag can automatically fix:
- ✅ Trailing whitespace (removed)
- ✅ Multiple blank lines (reduced to max 2)
- ✅ Missing file-ending newline (added)

Cannot auto-fix (requires manual intervention):
- ❌ Multiple H1 headings
- ❌ Skipped heading levels
- ❌ Code blocks without language tags
- ❌ Long lines

## Integration with CI/CD

Add to your CI/CD workflow:

```yaml
# .github/workflows/lint.yml
- name: Lint Markdown Files
  run: |
    python3 src/event_manager.py docs lint-markdown --all
```

## Testing

Run tests:

```bash
python3 tests/test_markdown_linting.py
```

All 10 tests should pass ✅

## Configuration

The linter uses these defaults:
- Max line length: 120 characters (for prose)
- Max consecutive blank lines: 2
- Code blocks must have language tags
- Files must end with newline

No configuration file needed - sensible defaults follow best practices.

## Files Added

- `scripts/lint_markdown.py` - Main linting script
- `tests/test_markdown_linting.py` - Comprehensive test suite
- Updates to:
  - `src/modules/docs_runner.py` - CLI integration
  - `src/event_manager.py` - Help text
  - `scripts/README.md` - Documentation

## Learn More

- Run `python3 scripts/lint_markdown.py --help` for detailed help
- Check `scripts/README.md` for full documentation
- See `tests/test_markdown_linting.py` for usage examples
