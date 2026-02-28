"""
Simple test script to verify the API endpoints work correctly
"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from fastapi.testclient import TestClient
from app import app
import json

client = TestClient(app)

def test_send_data_endpoint():
    """Test POST /send-data endpoint"""
    print("Testing POST /send-data endpoint...")
    
    # Test valid data
    response = client.post("/send-data", json={
        "time": [0.0, 0.001, 0.002, 0.003, 0.004],
        "acceleration": [1.0, 2.0, 1.5, 0.5, 0.2]
    })
    
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    print("✓ Valid data accepted")
    
    # Test invalid JSON (mismatched array lengths)
    response = client.post("/send-data", json={
        "time": [0.0, 0.001],
        "acceleration": [1.0]
    })
    
    assert response.status_code == 400
    print("✓ Mismatched array lengths rejected")
    
    # Test empty arrays
    response = client.post("/send-data", json={
        "time": [],
        "acceleration": []
    })
    
    assert response.status_code == 400
    print("✓ Empty arrays rejected")
    
    print("POST /send-data endpoint: PASSED\n")

def test_get_data_endpoint():
    """Test GET /get-data endpoint"""
    print("Testing GET /get-data endpoint...")
    
    response = client.get("/get-data")
    
    assert response.status_code == 200
    data = response.json()
    assert "new_data_available" in data
    assert "damping_factor" in data
    assert "natural_frequency" in data
    assert "lifetime_time" in data
    assert "average_lifetime" in data
    assert "ai_lifetime" in data
    print("✓ Response contains all required fields")
    
    print("GET /get-data endpoint: PASSED\n")

def test_full_refresh_endpoint():
    """Test GET /full-refresh endpoint"""
    print("Testing GET /full-refresh endpoint...")
    
    response = client.get("/full-refresh")
    
    assert response.status_code == 200
    data = response.json()
    assert "time" in data
    assert "acceleration" in data
    assert "frequency" in data
    assert "amplitude" in data
    assert "damping_factor" in data
    assert "natural_frequency" in data
    assert "lifetime_time" in data
    assert "lifetime_freq" in data
    assert "lifetime_natural" in data
    assert "lifetime_damping" in data
    assert "average_lifetime" in data
    assert "ai_lifetime" in data
    print("✓ Response contains all required fields")
    
    print("GET /full-refresh endpoint: PASSED\n")

def test_data_flow():
    """Test complete data flow: send -> process -> retrieve"""
    print("Testing complete data flow...")
    
    # Send data
    response = client.post("/send-data", json={
        "time": [0.0, 0.001, 0.002, 0.003, 0.004, 0.005],
        "acceleration": [10.0, 8.0, 6.0, 4.0, 2.0, 1.0]
    })
    assert response.status_code == 200
    print("✓ Data sent successfully")
    
    # Get data (should have new_data_available = True initially)
    response = client.get("/get-data")
    assert response.status_code == 200
    data = response.json()
    # Note: new_data_available might be False if already retrieved
    print(f"✓ Data retrieved (new_data_available: {data['new_data_available']})")
    
    # Full refresh should return complete data
    response = client.get("/full-refresh")
    assert response.status_code == 200
    data = response.json()
    assert len(data["time"]) > 0
    assert len(data["acceleration"]) > 0
    print("✓ Full refresh returns complete dataset")
    
    print("Complete data flow: PASSED\n")

if __name__ == "__main__":
    print("=" * 60)
    print("API Endpoint Tests")
    print("=" * 60 + "\n")
    
    try:
        test_send_data_endpoint()
        test_get_data_endpoint()
        test_full_refresh_endpoint()
        test_data_flow()
        
        print("=" * 60)
        print("ALL TESTS PASSED ✓")
        print("=" * 60)
    except AssertionError as e:
        print(f"\n✗ TEST FAILED: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
