#!/usr/bin/env python3
"""
Demo: Workflow Dispatch Options Display

This script demonstrates how the workflow launcher now displays
dispatch options when viewing workflow runs.
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))


def demo_without_inputs():
    """Show example of runs without dispatch inputs (scheduled runs)"""
    print("=" * 80)
    print("EXAMPLE: Workflow runs WITHOUT dispatch options (scheduled runs)")
    print("=" * 80)
    print("\nRecent runs of workflow 'scrape-events':")
    print("-" * 80)
    
    print("Run #12346: completed / success")
    print("  Branch: main, Event: schedule, Created: 2024-01-17T03:00:00Z")
    print()
    
    print("Run #12345: completed / success")
    print("  Branch: main, Event: push, Created: 2024-01-17T02:30:00Z")
    print()
    
    print("-" * 80)


def demo_with_inputs():
    """Show example of runs with dispatch inputs (manually triggered)"""
    print("\n" + "=" * 80)
    print("EXAMPLE: Workflow runs WITH dispatch options (manually triggered)")
    print("=" * 80)
    print("\nRecent runs of workflow 'scrape-events':")
    print("-" * 80)
    
    print("Run #12348: in_progress / -")
    print("  Branch: main, Event: workflow_dispatch, Created: 2024-01-17T10:30:00Z")
    print("  Dispatch Options:")
    print("    • task: scrape-and-deploy")
    print("    • force_scrape: true")
    print("    • event_ids: pending_123,pending_456")
    print()
    
    print("Run #12347: completed / success")
    print("  Branch: main, Event: workflow_dispatch, Created: 2024-01-17T10:00:00Z")
    print("  Dispatch Options:")
    print("    • task: review-pending")
    print("    • event_ids: all")
    print("    • auto_publish_pattern: pending_*")
    print()
    
    print("Run #12346: completed / success")
    print("  Branch: main, Event: schedule, Created: 2024-01-17T03:00:00Z")
    print()
    
    print("-" * 80)


def demo_lint_workflow():
    """Show example with lint workflow having multiple choice options"""
    print("\n" + "=" * 80)
    print("EXAMPLE: Lint workflow with multiple dispatch options")
    print("=" * 80)
    print("\nRecent runs of workflow 'lint':")
    print("-" * 80)
    
    print("Run #12350: completed / success")
    print("  Branch: preview, Event: workflow_dispatch, Created: 2024-01-17T11:00:00Z")
    print("  Dispatch Options:")
    print("    • fail_on_python_errors: true")
    print("    • fail_on_js_errors: false")
    print("    • fail_on_json_errors: true")
    print("    • fail_on_style_issues: false")
    print()
    
    print("Run #12349: completed / failure")
    print("  Branch: feature/new-feature, Event: workflow_dispatch, Created: 2024-01-17T10:45:00Z")
    print("  Dispatch Options:")
    print("    • fail_on_python_errors: true")
    print("    • fail_on_js_errors: true")
    print("    • fail_on_json_errors: true")
    print("    • fail_on_style_issues: true")
    print()
    
    print("-" * 80)


def main():
    print("\n" + "🎯" * 40)
    print("WORKFLOW DISPATCH OPTIONS DISPLAY DEMO")
    print("🎯" * 40)
    print("\nThis demonstrates the new feature that shows workflow dispatch options")
    print("when viewing workflow runs in the 'All workflows' overview.")
    print()
    print("Key improvements:")
    print("  ✓ Shows 'event' type (workflow_dispatch, schedule, push, etc.)")
    print("  ✓ Displays dispatch options for manually triggered workflows")
    print("  ✓ Clear formatting with bullet points for each option")
    print("  ✓ Only shows dispatch options for workflow_dispatch events")
    print()
    
    demo_without_inputs()
    demo_with_inputs()
    demo_lint_workflow()
    
    print("\n" + "=" * 80)
    print("USAGE")
    print("=" * 80)
    print("\nTo view workflow runs with dispatch options in real use:")
    print("  $ python3 src/modules/workflow_launcher.py status scrape-events")
    print("  $ python3 src/modules/workflow_launcher.py status lint --limit 10")
    print()
    print("To trigger a workflow with options:")
    print("  $ python3 src/modules/workflow_launcher.py run scrape-events \\")
    print("      --branch main \\")
    print("      --input task=scrape-and-deploy \\")
    print("      --input force_scrape=true")
    print()
    print("=" * 80)
    print("\n✅ Demo completed successfully!")


if __name__ == '__main__':
    main()
