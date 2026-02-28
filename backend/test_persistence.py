#!/usr/bin/env python3
"""
Test data persistence across server restarts
"""
import sys
import os
import json
import time

sys.path.insert(0, os.path.dirname(__file__))

from app import DATA_STORE_PATH, init_data_store, save_data_store, load_data_store, append_data

def test_persistence():
    """Test that data persists across application restarts"""
    print("Testing data persistence across restarts...\n")
    
    # Step 1: Initialize with fresh data
    print("Step 1: Initializing data store...")
    initial_data = init_data_store()
    save_data_store(initial_data)
    print("✓ Data store initialized")
    
    # Step 2: Add some test data
    print("\nStep 2: Adding test data...")
    test_time = [0.0, 0.001, 0.002, 0.003, 0.004]
    test_acceleration = [10.0, 8.0, 6.0, 4.0, 2.0]
    append_data(test_time, test_acceleration)
    print(f"✓ Added {len(test_time)} data points")
    
    # Step 3: Verify data was saved
    print("\nStep 3: Verifying data was saved...")
    data = load_data_store()
    assert data["time"] == test_time, "Time data mismatch"
    assert data["acceleration"] == test_acceleration, "Acceleration data mismatch"
    assert data["new_data_available"] == True, "Flag should be True"
    print("✓ Data saved correctly")
    
    # Step 4: Simulate server restart by reloading from file
    print("\nStep 4: Simulating server restart (reloading from file)...")
    # Clear any in-memory state by reloading
    reloaded_data = load_data_store()
    print("✓ Data reloaded from file")
    
    # Step 5: Verify data persisted
    print("\nStep 5: Verifying data persisted after restart...")
    assert reloaded_data["time"] == test_time, "Time data not persisted"
    assert reloaded_data["acceleration"] == test_acceleration, "Acceleration data not persisted"
    assert reloaded_data["new_data_available"] == True, "Flag not persisted"
    print("✓ All data persisted correctly")
    
    # Step 6: Add more data after "restart"
    print("\nStep 6: Adding more data after restart...")
    more_time = [0.005, 0.006]
    more_acceleration = [1.0, 0.5]
    append_data(more_time, more_acceleration)
    print(f"✓ Added {len(more_time)} more data points")
    
    # Step 7: Verify cumulative data
    print("\nStep 7: Verifying cumulative data...")
    final_data = load_data_store()
    expected_time = test_time + more_time
    expected_acceleration = test_acceleration + more_acceleration
    assert final_data["time"] == expected_time, "Cumulative time data incorrect"
    assert final_data["acceleration"] == expected_acceleration, "Cumulative acceleration data incorrect"
    print(f"✓ Total data points: {len(final_data['time'])}")
    
    # Step 8: Verify file exists and is valid JSON
    print("\nStep 8: Verifying file integrity...")
    assert os.path.exists(DATA_STORE_PATH), "Data store file should exist"
    with open(DATA_STORE_PATH, 'r') as f:
        file_data = json.load(f)
    assert "time" in file_data, "File should contain 'time' field"
    assert "acceleration" in file_data, "File should contain 'acceleration' field"
    print("✓ File exists and contains valid JSON")
    
    print("\n" + "=" * 60)
    print("✓✓✓ DATA PERSISTENCE TEST PASSED ✓✓✓")
    print("=" * 60)

if __name__ == "__main__":
    try:
        test_persistence()
    except AssertionError as e:
        print(f"\n✗ TEST FAILED: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
