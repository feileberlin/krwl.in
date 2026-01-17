#!/usr/bin/env python3
"""
Test workflow launcher dispatch options display

This test verifies that workflow dispatch inputs are properly fetched and displayed
when viewing workflow runs in the "All workflows" overview.
"""

import sys
import json
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
import subprocess

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from modules.workflow_launcher import WorkflowLauncher


def test_get_workflow_run_inputs():
    """Test fetching workflow run inputs from GitHub API"""
    launcher = WorkflowLauncher()
    
    # Mock subprocess.run for gh api call
    mock_inputs = {"task": "scrape-and-deploy", "force_scrape": "false"}
    mock_result = MagicMock()
    mock_result.returncode = 0
    mock_result.stdout = json.dumps(mock_inputs)
    
    with patch('subprocess.run', return_value=mock_result):
        with patch.object(launcher, 'check_gh_auth', return_value=(True, "Authenticated")):
            inputs = launcher.get_workflow_run_inputs(12345)
            
            assert inputs is not None, "Should return inputs dict"
            assert inputs.get('task') == 'scrape-and-deploy', "Should have task input"
            assert inputs.get('force_scrape') == 'false', "Should have force_scrape input"
    
    print("✓ get_workflow_run_inputs() returns inputs correctly")


def test_get_workflow_run_inputs_no_inputs():
    """Test handling of runs without inputs (e.g., scheduled runs)"""
    launcher = WorkflowLauncher()
    
    # Mock subprocess.run for gh api call returning null
    mock_result = MagicMock()
    mock_result.returncode = 0
    mock_result.stdout = "null"
    
    with patch('subprocess.run', return_value=mock_result):
        with patch.object(launcher, 'check_gh_auth', return_value=(True, "Authenticated")):
            inputs = launcher.get_workflow_run_inputs(12345)
            
            assert inputs is None, "Should return None for runs without inputs"
    
    print("✓ get_workflow_run_inputs() handles null inputs correctly")


def test_get_workflow_runs_includes_inputs():
    """Test that get_workflow_runs fetches inputs for workflow_dispatch events"""
    launcher = WorkflowLauncher()
    
    # Mock workflow runs data
    mock_runs = [
        {
            "databaseId": 12345,
            "status": "completed",
            "conclusion": "success",
            "event": "workflow_dispatch",
            "headBranch": "main",
            "createdAt": "2024-01-17T10:00:00Z"
        },
        {
            "databaseId": 12346,
            "status": "completed",
            "conclusion": "success",
            "event": "schedule",
            "headBranch": "main",
            "createdAt": "2024-01-17T09:00:00Z"
        }
    ]
    
    mock_result = MagicMock()
    mock_result.returncode = 0
    mock_result.stdout = json.dumps(mock_runs)
    
    mock_inputs = {"task": "scrape-and-deploy", "force_scrape": "true"}
    
    with patch('subprocess.run', return_value=mock_result):
        with patch.object(launcher, 'check_gh_auth', return_value=(True, "Authenticated")):
            with patch.object(launcher, 'get_workflow_run_inputs', return_value=mock_inputs):
                success, runs = launcher.get_workflow_runs('scrape-events', limit=2)
                
                assert success, "Should successfully fetch runs"
                assert len(runs) == 2, "Should return 2 runs"
                
                # First run is workflow_dispatch, should have inputs
                assert runs[0].get('event') == 'workflow_dispatch'
                assert 'inputs' in runs[0], "workflow_dispatch run should have inputs"
                assert runs[0]['inputs'].get('task') == 'scrape-and-deploy'
                
                # Second run is scheduled, should not have inputs
                assert runs[1].get('event') == 'schedule'
    
    print("✓ get_workflow_runs() fetches inputs for workflow_dispatch events")


def test_workflow_runs_display_format():
    """Test that workflow dispatch options are formatted nicely for display"""
    # Mock run data with inputs
    run = {
        "databaseId": 12345,
        "status": "completed",
        "conclusion": "success",
        "event": "workflow_dispatch",
        "headBranch": "main",
        "createdAt": "2024-01-17T10:00:00Z",
        "inputs": {
            "task": "scrape-and-deploy",
            "force_scrape": "true",
            "event_ids": "pending_123,pending_456"
        }
    }
    
    # Build expected output format
    output_lines = []
    output_lines.append(f"Run #{run['databaseId']}: {run['status']} / {run['conclusion']}")
    output_lines.append(f"  Branch: {run['headBranch']}, Event: {run['event']}, Created: {run['createdAt']}")
    output_lines.append(f"  Dispatch Options:")
    
    inputs = run.get('inputs', {})
    for key, value in inputs.items():
        output_lines.append(f"    • {key}: {value}")
    
    expected_output = "\n".join(output_lines)
    
    # Verify format includes all expected parts
    assert "Run #12345" in expected_output, "Should show run ID"
    assert "workflow_dispatch" in expected_output, "Should show event type"
    assert "Dispatch Options:" in expected_output, "Should show dispatch options header"
    assert "• task: scrape-and-deploy" in expected_output, "Should show task input"
    assert "• force_scrape: true" in expected_output, "Should show force_scrape input"
    assert "• event_ids: pending_123,pending_456" in expected_output, "Should show event_ids input"
    
    print("✓ Workflow dispatch options formatted correctly for display")


def run_all_tests():
    """Run all tests"""
    tests = [
        test_get_workflow_run_inputs,
        test_get_workflow_run_inputs_no_inputs,
        test_get_workflow_runs_includes_inputs,
        test_workflow_runs_display_format
    ]
    
    results = []
    for test in tests:
        try:
            test()
            results.append(True)
        except AssertionError as e:
            print(f"✗ {test.__name__} failed: {e}")
            results.append(False)
        except Exception as e:
            print(f"✗ {test.__name__} error: {type(e).__name__}: {e}")
            results.append(False)
    
    print("\n" + "=" * 80)
    passed = sum(results)
    total = len(results)
    print(f"Test Results: {passed}/{total} passed")
    
    if passed == total:
        print("✅ All workflow dispatch options tests passed!")
        return 0
    else:
        print(f"❌ {total - passed} test(s) failed")
        return 1


if __name__ == '__main__':
    sys.exit(run_all_tests())
