# Vibration data simulator
# This module generates synthetic vibration data for testing

import numpy as np
import asyncio
import aiohttp
from typing import Tuple


def generate_vibration_signal(
    duration: float = 1.0,
    sampling_rate: float = 1000.0,
    amplitude: float = 10.0,
    frequency: float = 50.0,
    damping: float = 0.05
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Generate damped sinusoidal vibration signal
    
    Uses the formula: x(t) = A * exp(-zeta * omega * t) * sin(omega * t)
    where:
    - A is the amplitude
    - zeta is the damping factor
    - omega is the angular frequency (2 * pi * frequency)
    - t is time
    
    Small random noise is added for realism.
    
    Args:
        duration: Signal duration in seconds (default: 1.0)
        sampling_rate: Samples per second (default: 1000.0)
        amplitude: Signal amplitude in m/s² (default: 10.0)
        frequency: Oscillation frequency in Hz (default: 50.0)
        damping: Damping factor (dimensionless, default: 0.05)
    
    Returns:
        tuple: (time, acceleration) where both are numpy arrays
            - time: Time values in seconds
            - acceleration: Acceleration values in m/s²
    
    Requirements: 13.1, 13.3, 13.4, 13.5
    """
    # Generate time array
    num_samples = int(duration * sampling_rate)
    time = np.linspace(0, duration, num_samples)
    
    # Calculate angular frequency
    omega = 2 * np.pi * frequency
    
    # Generate damped oscillation envelope
    envelope = amplitude * np.exp(-damping * omega * time)
    
    # Generate sinusoidal signal with damping
    signal = envelope * np.sin(omega * time)
    
    # Add small random noise for realism (1% of amplitude)
    noise = np.random.normal(0, amplitude * 0.01, len(time))
    acceleration = signal + noise
    
    return time, acceleration


async def run_simulator(
    backend_url: str = "http://localhost:8000",
    interval: float = 2.0,
    duration: float = 1.0,
    sampling_rate: float = 1000.0,
    amplitude: float = 10.0,
    frequency: float = 50.0,
    damping: float = 0.05
):
    """
    Continuously generate and send vibration data to backend
    
    This function runs indefinitely, generating signal chunks at regular
    intervals and sending them to the /send-data endpoint.
    
    Args:
        backend_url: Base URL of the backend API (default: "http://localhost:8000")
        interval: Time between data transmissions in seconds (default: 2.0)
        duration: Duration of each signal chunk in seconds (default: 1.0)
        sampling_rate: Samples per second (default: 1000.0)
        amplitude: Signal amplitude in m/s² (default: 10.0)
        frequency: Oscillation frequency in Hz (default: 50.0)
        damping: Damping factor (default: 0.05)
    
    Requirements: 13.2
    """
    print(f"Starting vibration simulator...")
    print(f"Backend URL: {backend_url}")
    print(f"Interval: {interval}s, Duration: {duration}s")
    print(f"Parameters: amplitude={amplitude}, frequency={frequency}Hz, damping={damping}")
    print(f"Press Ctrl+C to stop\n")
    
    async with aiohttp.ClientSession() as session:
        iteration = 0
        while True:
            try:
                # Generate vibration signal
                time, acceleration = generate_vibration_signal(
                    duration=duration,
                    sampling_rate=sampling_rate,
                    amplitude=amplitude,
                    frequency=frequency,
                    damping=damping
                )
                
                # Prepare payload
                payload = {
                    "time": time.tolist(),
                    "acceleration": acceleration.tolist()
                }
                
                # Send data to backend
                async with session.post(
                    f"{backend_url}/send-data",
                    json=payload
                ) as response:
                    if response.status == 200:
                        result = await response.json()
                        iteration += 1
                        print(f"[{iteration}] Data sent successfully: {result['message']}")
                    else:
                        error_text = await response.text()
                        print(f"[{iteration}] Error: HTTP {response.status} - {error_text}")
                
            except aiohttp.ClientError as e:
                print(f"Network error: {e}")
            except Exception as e:
                print(f"Unexpected error: {e}")
            
            # Wait for next interval
            await asyncio.sleep(interval)


if __name__ == "__main__":
    # Run the simulator with default parameters
    # Can be customized by modifying the parameters below
    asyncio.run(run_simulator(
        backend_url="http://localhost:8000",
        interval=2.0,
        duration=1.0,
        sampling_rate=1000.0,
        amplitude=10.0,
        frequency=50.0,
        damping=0.05
    ))
