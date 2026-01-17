# Workflow Dispatch Options Display

## Overview

This feature enhances the GitHub Actions workflow launcher to display the dispatch options (workflow inputs) that were selected when manually triggering a workflow via `workflow_dispatch` events.

## Problem Statement

When viewing workflow runs in the "All workflows" overview, it was not clear which dispatch options were chosen when manually triggering a workflow. This made it difficult to:
- Understand why a particular workflow run behaved differently
- Audit manual workflow triggers and their parameters
- Debug workflow issues related to input parameters

## Solution

The workflow launcher now:
1. Fetches workflow run details including dispatch inputs via GitHub API
2. Displays dispatch options for `workflow_dispatch` events in the status overview
3. Shows clear formatting with bullet points for each input parameter

## Implementation Details

### New Methods

**`get_workflow_run_inputs(run_id: int)`**
- Fetches workflow dispatch inputs for a specific run using GitHub API
- Uses `gh api repos/{owner}/{repo}/actions/runs/{run_id} --jq '.inputs'`
- Returns dictionary of inputs or None if not available
- Handles null/empty inputs gracefully

**Enhanced `get_workflow_runs(workflow_id: str, limit: int)`**
- Now includes `event` and `displayTitle` fields in the run data
- Automatically fetches inputs for each `workflow_dispatch` event
- Adds `inputs` field to runs that were manually triggered

### Display Format

**Before:**
```
Run #12345: completed / success (branch: main, created: 2024-01-17T10:00:00Z)
```

**After:**
```
Run #12345: completed / success
  Branch: main, Event: workflow_dispatch, Created: 2024-01-17T10:00:00Z
  Dispatch Options:
    • task: scrape-and-deploy
    • force_scrape: true
    • event_ids: pending_123,pending_456
```

### Event Types

The launcher now displays the event type for each run:
- `workflow_dispatch` - Manually triggered with inputs
- `schedule` - Triggered by cron schedule
- `push` - Triggered by git push
- `pull_request` - Triggered by PR

## Usage

### View Workflow Runs with Dispatch Options

```bash
# View recent runs of a workflow
python3 src/modules/workflow_launcher.py status scrape-events

# View more runs
python3 src/modules/workflow_launcher.py status scrape-events --limit 10

# View runs of lint workflow
python3 src/modules/workflow_launcher.py status lint
```

### Example Output

```
Recent runs of workflow 'scrape-events':
--------------------------------------------------------------------------------
Run #12348: in_progress / -
  Branch: main, Event: workflow_dispatch, Created: 2024-01-17T10:30:00Z
  Dispatch Options:
    • task: scrape-and-deploy
    • force_scrape: true
    • event_ids: pending_123,pending_456

Run #12347: completed / success
  Branch: main, Event: workflow_dispatch, Created: 2024-01-17T10:00:00Z
  Dispatch Options:
    • task: review-pending
    • event_ids: all

Run #12346: completed / success
  Branch: main, Event: schedule, Created: 2024-01-17T03:00:00Z

--------------------------------------------------------------------------------
```

## Testing

### Run Tests

```bash
# Run comprehensive tests
python3 tests/test_workflow_inputs.py

# Run with verbose output
python3 tests/test_workflow_inputs.py --verbose
```

### Run Demo

```bash
# View demo examples
python3 examples/demo_workflow_inputs.py
```

## Benefits

1. **Transparency** - See exactly what options were chosen for each workflow run
2. **Debugging** - Easier to debug issues related to specific input combinations
3. **Auditing** - Track which manual triggers used which parameters
4. **Documentation** - Clear examples of how workflows were triggered

## Technical Notes

### API Efficiency

- The implementation only fetches inputs for `workflow_dispatch` events
- Other event types (schedule, push, etc.) skip the API call
- Uses GitHub CLI's built-in authentication
- Includes proper timeout and error handling

### Error Handling

- Gracefully handles missing inputs (returns None)
- Handles null inputs from scheduled runs
- Includes timeout protection (10 seconds per API call)
- Sanitizes sensitive information in error messages

### Dependencies

- Requires GitHub CLI (`gh`) installed and authenticated
- Uses `gh api` command for fetching workflow run details
- Uses `gh run list` for listing workflow runs

## Files Modified

1. **src/modules/workflow_launcher.py**
   - Added `get_workflow_run_inputs()` method
   - Enhanced `get_workflow_runs()` to fetch inputs
   - Improved status display formatting

2. **tests/test_workflow_inputs.py** (new)
   - Comprehensive test suite with 4 tests
   - Mocks GitHub API calls
   - Tests input fetching, display formatting, and edge cases

3. **examples/demo_workflow_inputs.py** (new)
   - Interactive demo showing the feature in action
   - Example outputs for different workflow types

4. **features.json**
   - Updated workflow-launcher feature entry
   - Added test file reference
   - Added test instructions

## Future Enhancements

Possible improvements for future versions:
- Add input filtering/search in status command
- Support for displaying workflow outputs
- Export workflow run data to JSON/CSV
- Integration with TUI for interactive workflow run browsing
