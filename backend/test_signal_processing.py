#!/usr/bin/env python3
"""
Quick verification test for signal processing functions
"""

import numpy as np
import sys
sys.path.insert(0, '.')

from signal_processing import compute_fft, calculate_damping_factor, detect_natural_frequency

def test_compute_fft():
    """Test FFT computation with a simple sinusoidal signal"""
    print("Testing compute_fft()...")
    
    # Generate a simple 50 Hz sinusoidal signal
    duration = 1.0
    sampling_rate = 1000.0
    frequency = 50.0
    
    t = np.linspace(0, duration, int(duration * sampling_rate))
    signal = 10.0 * np.sin(2 * np.pi * frequency * t)
    
    freq, amplitude = compute_fft(t, signal)
    
    # Verify outputs
    assert len(freq) > 0, "Frequency array should not be empty"
    assert len(amplitude) > 0, "Amplitude array should not be empty"
    assert len(freq) == len(amplitude), "Frequency and amplitude arrays should have same length"
    assert np.all(freq >= 0), "All frequencies should be non-negative"
    assert np.all(amplitude >= 0), "All amplitudes should be non-negative"
    
    # Check that frequencies are monotonically increasing
    assert np.all(np.diff(freq) >= 0), "Frequencies should be monotonically increasing"
    
    print("✓ compute_fft() passed basic tests")
    
    # Test edge cases
    empty_time = np.array([])
    empty_accel = np.array([])
    freq_empty, amp_empty = compute_fft(empty_time, empty_accel)
    assert len(freq_empty) == 0 and len(amp_empty) == 0, "Empty arrays should return empty results"
    
    single_time = np.array([0.0])
    single_accel = np.array([5.0])
    freq_single, amp_single = compute_fft(single_time, single_accel)
    assert len(freq_single) == 1 and len(amp_single) == 1, "Single element should return single element"
    
    print("✓ compute_fft() edge cases passed")

def test_calculate_damping_factor():
    """Test damping factor calculation with a damped oscillation"""
    print("\nTesting calculate_damping_factor()...")
    
    # Generate a damped sinusoidal signal
    duration = 1.0
    sampling_rate = 1000.0
    frequency = 50.0
    damping = 0.1
    amplitude = 10.0
    
    t = np.linspace(0, duration, int(duration * sampling_rate))
    omega = 2 * np.pi * frequency
    signal = amplitude * np.exp(-damping * omega * t) * np.sin(omega * t)
    
    zeta = calculate_damping_factor(t, signal)
    
    # Verify output
    assert 0 <= zeta < 1, f"Damping factor should be between 0 and 1 for underdamped systems, got {zeta}"
    
    print(f"✓ calculate_damping_factor() returned zeta = {zeta:.4f}")
    
    # Test edge cases
    empty_accel = np.array([])
    zeta_empty = calculate_damping_factor(np.array([]), empty_accel)
    assert zeta_empty == 0.05, "Empty array should return default damping"
    
    single_accel = np.array([5.0])
    zeta_single = calculate_damping_factor(np.array([0.0]), single_accel)
    assert zeta_single == 0.05, "Single element should return default damping"
    
    print("✓ calculate_damping_factor() edge cases passed")

def test_detect_natural_frequency():
    """Test natural frequency detection"""
    print("\nTesting detect_natural_frequency()...")
    
    # Generate a signal with known frequency
    duration = 1.0
    sampling_rate = 1000.0
    target_frequency = 50.0
    
    t = np.linspace(0, duration, int(duration * sampling_rate))
    signal = 10.0 * np.sin(2 * np.pi * target_frequency * t)
    
    # Compute FFT
    freq, amplitude = compute_fft(t, signal)
    
    # Detect natural frequency
    natural_freq = detect_natural_frequency(freq, amplitude)
    
    # Verify output
    assert natural_freq > 0, "Natural frequency should be greater than 0 (DC excluded)"
    assert 45 <= natural_freq <= 55, f"Natural frequency should be close to 50 Hz, got {natural_freq:.2f} Hz"
    
    print(f"✓ detect_natural_frequency() returned {natural_freq:.2f} Hz (expected ~50 Hz)")
    
    # Test edge cases
    empty_freq = np.array([])
    empty_amp = np.array([])
    nat_freq_empty = detect_natural_frequency(empty_freq, empty_amp)
    assert nat_freq_empty == 0.0, "Empty arrays should return 0.0"
    
    single_amp = np.array([5.0])
    nat_freq_single = detect_natural_frequency(np.array([0.0]), single_amp)
    assert nat_freq_single == 0.0, "Single element should return 0.0"
    
    print("✓ detect_natural_frequency() edge cases passed")

if __name__ == "__main__":
    print("=" * 60)
    print("Signal Processing Functions Verification")
    print("=" * 60)
    
    try:
        test_compute_fft()
        test_calculate_damping_factor()
        test_detect_natural_frequency()
        
        print("\n" + "=" * 60)
        print("✓ All tests passed successfully!")
        print("=" * 60)
    except AssertionError as e:
        print(f"\n✗ Test failed: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
