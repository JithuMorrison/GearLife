# Test script for simulator module
import numpy as np
from simulator import generate_vibration_signal

# Test 1: Basic signal generation
print("Test 1: Basic signal generation")
time, acceleration = generate_vibration_signal(
    duration=1.0,
    sampling_rate=1000.0,
    amplitude=10.0,
    frequency=50.0,
    damping=0.05
)

print(f"  Time array length: {len(time)}")
print(f"  Acceleration array length: {len(acceleration)}")
print(f"  Time range: [{time[0]:.3f}, {time[-1]:.3f}] seconds")
print(f"  Acceleration range: [{np.min(acceleration):.3f}, {np.max(acceleration):.3f}] m/s²")
print(f"  Arrays have equal length: {len(time) == len(acceleration)}")
print()

# Test 2: Different parameters
print("Test 2: Different amplitude")
time2, acceleration2 = generate_vibration_signal(
    duration=0.5,
    sampling_rate=500.0,
    amplitude=20.0,
    frequency=100.0,
    damping=0.1
)

print(f"  Time array length: {len(time2)}")
print(f"  Acceleration array length: {len(acceleration2)}")
print(f"  Max acceleration (higher amplitude): {np.max(np.abs(acceleration2)):.3f} m/s²")
print()

# Test 3: Verify damping effect
print("Test 3: Verify damping effect (amplitude should decay)")
time3, acceleration3 = generate_vibration_signal(
    duration=2.0,
    sampling_rate=1000.0,
    amplitude=10.0,
    frequency=50.0,
    damping=0.1
)

# Check first and last 100 samples
first_100_rms = np.sqrt(np.mean(acceleration3[:100]**2))
last_100_rms = np.sqrt(np.mean(acceleration3[-100:]**2))

print(f"  RMS of first 100 samples: {first_100_rms:.3f} m/s²")
print(f"  RMS of last 100 samples: {last_100_rms:.3f} m/s²")
print(f"  Amplitude decayed: {first_100_rms > last_100_rms}")
print()

# Test 4: Verify output format (should be numpy arrays)
print("Test 4: Verify output types")
print(f"  Time is numpy array: {isinstance(time, np.ndarray)}")
print(f"  Acceleration is numpy array: {isinstance(acceleration, np.ndarray)}")
print()

print("All tests completed successfully!")
