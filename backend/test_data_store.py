"""
Test data store management functions
"""
import os
import json
import sys

# Add backend directory to path
sys.path.insert(0, os.path.dirname(__file__))

from app import init_data_store, load_data_store, save_data_store, append_data, DATA_STORE_PATH

def test_init_data_store():
    """Test that init_data_store creates correct structure"""
    data = init_data_store()
    
    # Check all required fields exist
    required_fields = [
        "time", "acceleration", "frequency", "amplitude",
        "damping_factor", "natural_frequency",
        "lifetime_time", "lifetime_freq", "lifetime_natural", "lifetime_damping",
        "average_lifetime", "ai_lifetime", "new_data_available"
    ]
    
    for field in required_fields:
        assert field in data, f"Missing field: {field}"
    
    # Check default values
    assert data["time"] == []
    assert data["acceleration"] == []
    assert data["new_data_available"] == False
    assert data["damping_factor"] == 0.0
    
    print("✓ test_init_data_store passed")

def test_save_and_load():
    """Test saving and loading data store"""
    # Create test data
    test_data = init_data_store()
    test_data["time"] = [1.0, 2.0, 3.0]
    test_data["acceleration"] = [0.5, 1.0, 1.5]
    test_data["damping_factor"] = 0.05
    
    # Save data
    save_data_store(test_data)
    
    # Load data
    loaded_data = load_data_store()
    
    # Verify data matches
    assert loaded_data["time"] == [1.0, 2.0, 3.0]
    assert loaded_data["acceleration"] == [0.5, 1.0, 1.5]
    assert loaded_data["damping_factor"] == 0.05
    
    print("✓ test_save_and_load passed")

def test_append_data():
    """Test appending data to store"""
    # Initialize with empty data
    initial_data = init_data_store()
    save_data_store(initial_data)
    
    # Append first batch
    append_data([1.0, 2.0], [0.5, 1.0])
    
    # Load and verify
    data = load_data_store()
    assert len(data["time"]) == 2
    assert len(data["acceleration"]) == 2
    assert data["time"] == [1.0, 2.0]
    assert data["acceleration"] == [0.5, 1.0]
    assert data["new_data_available"] == True
    
    # Append second batch
    append_data([3.0, 4.0], [1.5, 2.0])
    
    # Load and verify appending worked
    data = load_data_store()
    assert len(data["time"]) == 4
    assert len(data["acceleration"]) == 4
    assert data["time"] == [1.0, 2.0, 3.0, 4.0]
    assert data["acceleration"] == [0.5, 1.0, 1.5, 2.0]
    assert data["new_data_available"] == True
    
    print("✓ test_append_data passed")

def test_corrupted_file_recovery():
    """Test that corrupted files are handled gracefully"""
    # Write corrupted JSON
    with open(DATA_STORE_PATH, 'w') as f:
        f.write("{ invalid json }")
    
    # Load should recover with defaults
    data = load_data_store()
    
    # Verify we got default structure
    assert "time" in data
    assert "acceleration" in data
    assert data["time"] == []
    
    # Verify backup was created
    backup_path = DATA_STORE_PATH + ".backup"
    assert os.path.exists(backup_path), "Backup file should be created"
    
    # Clean up backup
    if os.path.exists(backup_path):
        os.remove(backup_path)
    
    print("✓ test_corrupted_file_recovery passed")

if __name__ == "__main__":
    print("Running data store management tests...\n")
    
    try:
        test_init_data_store()
        test_save_and_load()
        test_append_data()
        test_corrupted_file_recovery()
        
        print("\n✅ All tests passed!")
    except AssertionError as e:
        print(f"\n❌ Test failed: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)
