# Integration test for simulator - tests connection to backend
# This test requires the backend server to be running

import asyncio
import aiohttp
from simulator import generate_vibration_signal

async def test_simulator_connection():
    """Test that simulator can send data to backend"""
    backend_url = "http://localhost:8000"
    
    print("Testing simulator connection to backend...")
    print(f"Backend URL: {backend_url}")
    print("Note: This test requires the backend server to be running on port 8000\n")
    
    try:
        # Generate a test signal
        time, acceleration = generate_vibration_signal(
            duration=0.5,
            sampling_rate=500.0,
            amplitude=10.0,
            frequency=50.0,
            damping=0.05
        )
        
        # Prepare payload
        payload = {
            "time": time.tolist(),
            "acceleration": acceleration.tolist()
        }
        
        print(f"Generated signal: {len(time)} samples")
        
        # Try to send data to backend
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{backend_url}/send-data",
                json=payload,
                timeout=aiohttp.ClientTimeout(total=5)
            ) as response:
                if response.status == 200:
                    result = await response.json()
                    print(f"✓ Success: {result['message']}")
                    print(f"✓ Status: {result['status']}")
                    return True
                else:
                    error_text = await response.text()
                    print(f"✗ Error: HTTP {response.status}")
                    print(f"  Response: {error_text}")
                    return False
                    
    except aiohttp.ClientConnectorError:
        print("✗ Connection failed: Backend server is not running")
        print("  To start the backend server, run: python app.py")
        return False
    except asyncio.TimeoutError:
        print("✗ Connection timeout: Backend server did not respond")
        return False
    except Exception as e:
        print(f"✗ Unexpected error: {e}")
        return False

if __name__ == "__main__":
    result = asyncio.run(test_simulator_connection())
    if result:
        print("\n✓ Simulator integration test passed!")
    else:
        print("\n✗ Simulator integration test failed")
        print("  Make sure the backend server is running: python app.py")
