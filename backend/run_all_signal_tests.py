#!/usr/bin/env python3
"""
Comprehensive test runner for all signal processing functions
"""

import sys
import subprocess

def run_test_file(filename, description):
    """Run a test file and report results"""
    print(f"\n{'=' * 70}")
    print(f"Running: {description}")
    print('=' * 70)
    
    result = subprocess.run(
        [sys.executable, filename],
        capture_output=False,
        text=True
    )
    
    if result.returncode != 0:
        print(f"\n✗ {description} FAILED")
        return False
    
    print(f"\n✓ {description} PASSED")
    return True

def main():
    print("=" * 70)
    print("SIGNAL PROCESSING TEST SUITE")
    print("=" * 70)
    
    test_files = [
        ("backend/test_signal_processing.py", "Core Signal Processing Tests"),
        ("backend/test_lifetime_functions.py", "Lifetime Calculation Tests")
    ]
    
    results = []
    for filename, description in test_files:
        success = run_test_file(filename, description)
        results.append((description, success))
    
    # Summary
    print("\n" + "=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)
    
    all_passed = True
    for description, success in results:
        status = "✓ PASSED" if success else "✗ FAILED"
        print(f"{status}: {description}")
        if not success:
            all_passed = False
    
    print("=" * 70)
    
    if all_passed:
        print("\n✓✓✓ ALL SIGNAL PROCESSING TESTS PASSED ✓✓✓\n")
        return 0
    else:
        print("\n✗✗✗ SOME TESTS FAILED ✗✗✗\n")
        return 1

if __name__ == "__main__":
    sys.exit(main())
