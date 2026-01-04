# Fix: Review Pending Events Workflow Issue

## Problem Statement

The "review-pending" task in the website-maintenance workflow was failing with an error message indicating the job "is not allowed" to run.

## Root Cause Analysis

### The Issue

When a user manually triggered the workflow with `task: 'review-pending'`:

1. The workflow would start and run the `discover-capabilities` job successfully
2. The `scrape-events` job would be **skipped** because its condition didn't match:
   ```yaml
   if: |
     (github.event_name == 'schedule' || 
      github.event.inputs.task == 'scrape-only' || 
      github.event.inputs.task == 'scrape-and-deploy' ||
      github.event.inputs.force_scrape == 'true')
   ```
   Note: `task == 'review-pending'` is NOT in this list
3. The `review-pending` job would then fail with "is not allowed" because:
   ```yaml
   needs: [discover-capabilities, scrape-events]
   ```
   GitHub Actions requires ALL jobs in the `needs` list to complete successfully (not be skipped or failed) unless explicitly handled

### Why This Happened

The original implementation assumed that `scrape-events` might have new events to review. However:
- The `review-pending` task is meant to review **already-pending** events
- Scraping new events is a separate operation
- These two operations should be independent

## Solution

### Changes Made

**File:** `.github/workflows/website-maintenance.yml`

**Before:**
```yaml
review-pending:
  name: Review Pending Events
  runs-on: ubuntu-latest
  needs: [discover-capabilities, scrape-events]
  if: |
    always() &&
    (github.event.inputs.task == 'review-pending' ||
     (github.event.inputs.auto_publish_pattern != '' && github.event.inputs.auto_publish_pattern != null))
```

**After:**
```yaml
review-pending:
  name: Review Pending Events
  runs-on: ubuntu-latest
  needs: discover-capabilities
  if: |
    github.event.inputs.task == 'review-pending' ||
    (github.event.inputs.auto_publish_pattern != '' && github.event.inputs.auto_publish_pattern != null)
```

### Key Changes

1. **Removed `scrape-events` from dependencies**: Changed `needs: [discover-capabilities, scrape-events]` to `needs: discover-capabilities`
2. **Removed `always()` wrapper**: No longer needed since we're not dealing with skipped dependencies
3. **Updated comment**: Removed reference to scrape-events job in the checkout step

## Verification

### Job Dependency Graph (After Fix)

```
discover-capabilities
├── scrape-events
│   ├── update-events
│   └── full-rebuild
│       └── deploy
├── show-info
└── review-pending (FIXED - now independent)
```

### Expected Behavior

Now when a user triggers the workflow with `task: 'review-pending'`:

1. ✅ `discover-capabilities` runs (provides workflow info)
2. ⏭️ `scrape-events` is skipped (not needed for review)
3. ✅ `review-pending` runs successfully (only needs discover-capabilities)
4. If events are published:
   - Changes are committed and pushed to `assets/json/events.json`
   - This triggers a new workflow run via push event
   - The new run handles deployment automatically

### Use Cases

The fix enables these workflows:

**1. Review Pending Events Only**
```
User → Trigger workflow with task='review-pending'
     → review-pending job runs
     → Events published to assets/json/events.json
     → Push triggers deployment workflow
```

**2. Scrape and Review (if needed)**
```
User → Trigger workflow with task='scrape-and-deploy'
     → scrape-events runs (new events → pending)
User → Trigger workflow with task='review-pending'
     → review-pending job runs (reviews newly scraped events)
```

**3. Auto-publish Pattern**
```
User → Trigger workflow with auto_publish_pattern='pending_official_*'
     → review-pending job runs
     → All matching events auto-published
```

## Testing

To test this fix:

1. Navigate to GitHub Actions → website-maintenance.yml
2. Click "Run workflow"
3. Select task: `review-pending`
4. Provide `event_ids` or `auto_publish_pattern`
5. Run workflow
6. Verify that the workflow completes successfully

## Impact

- **No breaking changes**: Other workflow tasks continue to work as before
- **Improved independence**: Review and scraping operations are now properly separated
- **Better error handling**: No more confusing "is not allowed" errors
- **Clearer intent**: Job dependencies now reflect actual requirements

## Related Files

- `.github/workflows/website-maintenance.yml` - Main workflow file (FIXED)
- `.github/workflows/README-website-maintenance.md` - Documentation
- `src/event_manager.py` - CLI that workflows call
- `src/modules/editor.py` - Editorial functionality

## Conclusion

This fix resolves the "is not allowed" error by removing an unnecessary dependency. The `review-pending` job now works independently, as intended, allowing users to review and publish pending events without requiring a scraping operation to have occurred first.
