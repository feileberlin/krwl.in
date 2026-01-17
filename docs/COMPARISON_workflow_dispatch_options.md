# Workflow Dispatch Options - Before & After Comparison

## Issue
Show GitHub workflow's chosen dispatch option in overview "All workflows" (showing runs)

## Before
When viewing workflow runs, only basic information was displayed:

```
Recent runs of workflow 'scrape-events':
--------------------------------------------------------------------------------
Run #12348: in_progress / - (branch: main, created: 2024-01-17T10:30:00Z)
Run #12347: completed / success (branch: main, created: 2024-01-17T10:00:00Z)
Run #12346: completed / success (branch: main, created: 2024-01-17T03:00:00Z)
--------------------------------------------------------------------------------
```

**Problems:**
- ❌ No indication of HOW the workflow was triggered (manual vs scheduled)
- ❌ No visibility into WHICH dispatch options were selected
- ❌ Difficult to debug issues related to specific input parameters
- ❌ No audit trail of manual workflow triggers

## After
Enhanced display shows event type and dispatch options:

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
    • auto_publish_pattern: pending_*

Run #12346: completed / success
  Branch: main, Event: schedule, Created: 2024-01-17T03:00:00Z

--------------------------------------------------------------------------------
```

**Benefits:**
- ✅ Shows event type (workflow_dispatch, schedule, push, etc.)
- ✅ Displays all dispatch options that were selected
- ✅ Clear bullet-point formatting for easy reading
- ✅ Only shows dispatch options for manually triggered workflows
- ✅ Easier to debug workflow issues
- ✅ Better audit trail for compliance

## Technical Changes

### 1. New Method: `get_workflow_run_inputs()`
```python
def get_workflow_run_inputs(self, run_id: int) -> Optional[Dict[str, str]]:
    """
    Get workflow dispatch inputs for a specific run using GitHub API
    
    Uses: gh api repos/{owner}/{repo}/actions/runs/{run_id} --jq '.inputs'
    Returns: Dictionary of inputs or None if not available
    """
```

### 2. Enhanced Method: `get_workflow_runs()`
```python
# Before: Only fetched basic fields
'databaseId,conclusion,status,createdAt,headBranch'

# After: Fetches event type and automatically adds inputs
'databaseId,conclusion,status,createdAt,headBranch,event,displayTitle'

# Plus: Automatically fetches inputs for workflow_dispatch events
for run in runs:
    if run.get('event') == 'workflow_dispatch':
        inputs = self.get_workflow_run_inputs(run.get('databaseId'))
        if inputs:
            run['inputs'] = inputs
```

### 3. Improved Display Format
```python
# Before: Single line
print(f"Run #{run.get('databaseId')}: {status} / {conclusion} (branch: {branch}, created: {created})")

# After: Multi-line with optional dispatch options
print(f"Run #{run.get('databaseId')}: {status} / {conclusion}")
print(f"  Branch: {branch}, Event: {event}, Created: {created}")
if inputs:
    print(f"  Dispatch Options:")
    for key, value in inputs.items():
        print(f"    • {key}: {value}")
```

## Real-World Use Cases

### Use Case 1: Debugging Failed Workflow
**Scenario:** A workflow run failed, but you don't remember which options you selected.

**Before:** You'd have to manually check the GitHub UI or git logs.

**After:** Simply run `python3 src/modules/workflow_launcher.py status scrape-events` and see:
```
Run #12349: completed / failure
  Branch: main, Event: workflow_dispatch, Created: 2024-01-17T10:45:00Z
  Dispatch Options:
    • fail_on_python_errors: true
    • fail_on_js_errors: true
    • fail_on_json_errors: true
    • fail_on_style_issues: true
```
Now you know it failed because all strict checks were enabled!

### Use Case 2: Audit Trail
**Scenario:** Management wants to know which manual deployments were forced.

**Before:** No easy way to track this from the CLI.

**After:** Run the status command and see all forced deployments:
```
Run #12350: completed / success
  Branch: main, Event: workflow_dispatch, Created: 2024-01-17T11:00:00Z
  Dispatch Options:
    • task: force-deploy
```

### Use Case 3: Learning from History
**Scenario:** A successful workflow run worked well, and you want to repeat it.

**Before:** Hard to remember what options you used.

**After:** Check the history and see exactly what worked:
```
Run #12347: completed / success
  Branch: main, Event: workflow_dispatch, Created: 2024-01-17T10:00:00Z
  Dispatch Options:
    • task: scrape-and-deploy
    • force_scrape: false
```

## Files Changed

1. **src/modules/workflow_launcher.py** (+48 lines)
   - Added `get_workflow_run_inputs()` method
   - Enhanced `get_workflow_runs()` to fetch inputs
   - Improved status display formatting

2. **tests/test_workflow_inputs.py** (new file, 195 lines)
   - Comprehensive test suite
   - 4/4 tests passing
   - Mock GitHub API calls

3. **examples/demo_workflow_inputs.py** (new file, 150 lines)
   - Interactive demo
   - Shows various scenarios
   - Usage examples

4. **docs/workflow-dispatch-options.md** (new file, 235 lines)
   - Complete documentation
   - API details
   - Usage instructions

5. **features.json** (updated)
   - Updated workflow-launcher feature entry
   - Added test file reference
   - Added test instructions

## Testing

All tests pass:
```
$ python3 tests/test_workflow_inputs.py
✓ get_workflow_run_inputs() returns inputs correctly
✓ get_workflow_run_inputs() handles null inputs correctly
✓ get_workflow_runs() fetches inputs for workflow_dispatch events
✓ Workflow dispatch options formatted correctly for display

Test Results: 4/4 passed
✅ All workflow dispatch options tests passed!
```

## Summary

This enhancement provides **full transparency** into workflow runs by displaying:
- **Event type** - How the workflow was triggered
- **Dispatch options** - Which inputs were selected
- **Clear formatting** - Easy to read and understand

The implementation is:
- **Minimal** - Only ~50 lines of core code
- **Efficient** - Only fetches inputs for workflow_dispatch events
- **Robust** - Handles errors and edge cases gracefully
- **Well-tested** - Comprehensive test coverage
- **Well-documented** - Examples and usage instructions

This makes workflow debugging, auditing, and management significantly easier!
