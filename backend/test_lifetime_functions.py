#!/usr/bin/env python3
"""
Unit tests for lifetime calculation functions
"""

import numpy as np
import sys
sys.path.insert(0, '.')

from signal_processing import (
    calculate_lifetime_time_domain,
    calculate_lifetime_frequency_domain,
    calculate_lifetime_natural_frequency,
    calculate_lifetime_damping,
    calculate_weighted_average_lifetime
)

def test_calculate_lifetime_time_domain():
    """Test time-domain lifetime calculation"""
    print("Testing calculate_lifetime_time_domain()...")
    
    # Test with valid parameters
    duration = 1.0
    sampling_rate = 1000.0
    t = np.linspace(0, duration, int(duration * sampling_rate))
    signal = 10.0 * np.exp(-0.1 * 2 * np.pi * 50 * t) * np.sin(2 * np.pi * 50 * t)
    
    zeta = 0.1
    omega_n = 2 * np.pi * 50  # 50 Hz
    
    lifetime = calculate_lifetime_time_domain(t, signal, zeta, omega_n)
    
    # Verify output is within reasonable bounds
    assert 10.0 <= lifetime <= 10000.0, f"Lifetime should be in range [10, 10000], got {lifetime}"
    assert lifetime > 0, "Lifetime should be positive"
    
    print(f"✓ calculate_lifetime_time_domain() returned {lifetime:.2f} hours")
    
    # Test edge cases
    empty_signal = np.array([])
    lifetime_empty = calculate_lifetime_time_domain(np.array([]), empty_signal, zeta, omega_n)
    assert lifetime_empty == 1000.0, "Empty signal should return default lifetime"
    
    # Test with zero omega_n
    lifetime_zero_omega = calculate_lifetime_time_domain(t, signal, zeta, 0.0)
    assert lifetime_zero_omega == 1000.0, "Zero omega_n should return default lifetime"
    
    print("✓ calculate_lifetime_time_domain() edge cases passed")

def test_calculate_lifetime_frequency_domain():
    """Test frequency-domain lifetime calculation"""
    print("\nTesting calculate_lifetime_frequency_domain()...")
    
    # Test with valid amplitude spectrum
    freq = np.linspace(0, 500, 501)
    amplitude = np.random.rand(501) * 10
    
    lifetime = calculate_lifetime_frequency_domain(freq, amplitude)
    
    # Verify output is within reasonable bounds
    assert 10.0 <= lifetime <= 10000.0, f"Lifetime should be in range [10, 10000], got {lifetime}"
    assert lifetime > 0, "Lifetime should be positive"
    
    print(f"✓ calculate_lifetime_frequency_domain() returned {lifetime:.2f} hours")
    
    # Test edge cases
    empty_amplitude = np.array([])
    lifetime_empty = calculate_lifetime_frequency_domain(np.array([]), empty_amplitude)
    assert lifetime_empty == 1000.0, "Empty amplitude should return default lifetime"
    
    # Test with zero energy
    zero_amplitude = np.zeros(100)
    lifetime_zero = calculate_lifetime_frequency_domain(freq[:100], zero_amplitude)
    assert lifetime_zero == 1000.0, "Zero energy should return default lifetime"
    
    print("✓ calculate_lifetime_frequency_domain() edge cases passed")

def test_calculate_lifetime_natural_frequency():
    """Test natural frequency shift lifetime calculation"""
    print("\nTesting calculate_lifetime_natural_frequency()...")
    
    # Test with frequency close to baseline
    natural_freq = 50.0
    lifetime = calculate_lifetime_natural_frequency(natural_freq)
    
    # Verify output is within reasonable bounds
    assert 10.0 <= lifetime <= 10000.0, f"Lifetime should be in range [10, 10000], got {lifetime}"
    assert lifetime > 0, "Lifetime should be positive"
    
    print(f"✓ calculate_lifetime_natural_frequency() returned {lifetime:.2f} hours for 50 Hz")
    
    # Test with frequency far from baseline
    natural_freq_shifted = 100.0
    lifetime_shifted = calculate_lifetime_natural_frequency(natural_freq_shifted)
    assert lifetime_shifted < lifetime, "Larger frequency shift should give shorter lifetime"
    
    print(f"✓ Shifted frequency (100 Hz) gives shorter lifetime: {lifetime_shifted:.2f} hours")
    
    # Test edge cases
    lifetime_zero = calculate_lifetime_natural_frequency(0.0)
    assert lifetime_zero == 1000.0, "Zero frequency should return default lifetime"
    
    print("✓ calculate_lifetime_natural_frequency() edge cases passed")

def test_calculate_lifetime_damping():
    """Test damping-based lifetime calculation"""
    print("\nTesting calculate_lifetime_damping()...")
    
    # Test with low damping
    zeta_low = 0.05
    lifetime_low = calculate_lifetime_damping(zeta_low)
    
    # Verify output is within reasonable bounds
    assert 10.0 <= lifetime_low <= 10000.0, f"Lifetime should be in range [10, 10000], got {lifetime_low}"
    assert lifetime_low > 0, "Lifetime should be positive"
    
    print(f"✓ calculate_lifetime_damping() returned {lifetime_low:.2f} hours for zeta=0.05")
    
    # Test with higher damping
    zeta_high = 0.2
    lifetime_high = calculate_lifetime_damping(zeta_high)
    assert lifetime_high < lifetime_low, "Higher damping should give shorter lifetime"
    
    print(f"✓ Higher damping (0.2) gives shorter lifetime: {lifetime_high:.2f} hours")
    
    # Test edge cases
    lifetime_zero = calculate_lifetime_damping(0.0)
    assert lifetime_zero == 1000.0, "Zero damping should return default lifetime"
    
    lifetime_negative = calculate_lifetime_damping(-0.1)
    assert lifetime_negative == 1000.0, "Negative damping should return default lifetime"
    
    print("✓ calculate_lifetime_damping() edge cases passed")

def test_calculate_weighted_average_lifetime():
    """Test weighted average lifetime calculation"""
    print("\nTesting calculate_weighted_average_lifetime()...")
    
    # Test with valid lifetime values
    L_time = 100.0
    L_freq = 200.0
    L_natural = 150.0
    L_damping = 250.0
    
    L_avg = calculate_weighted_average_lifetime(L_time, L_freq, L_natural, L_damping)
    
    # Verify the formula: L_avg = 0.25 * (L_time + L_freq + L_natural + L_damping)
    expected = 0.25 * L_time + 0.25 * L_freq + 0.25 * L_natural + 0.25 * L_damping
    assert abs(L_avg - expected) < 0.01, f"Average should be {expected}, got {L_avg}"
    
    print(f"✓ calculate_weighted_average_lifetime() returned {L_avg:.2f} hours (expected {expected:.2f})")
    
    # Test edge case: zero values
    L_avg_zero = calculate_weighted_average_lifetime(0.0, L_freq, L_natural, L_damping)
    assert L_avg_zero == 0.0, "Zero component should return 0.0"
    
    print("✓ calculate_weighted_average_lifetime() edge cases passed")

if __name__ == "__main__":
    print("=" * 60)
    print("Lifetime Calculation Functions Verification")
    print("=" * 60)
    
    try:
        test_calculate_lifetime_time_domain()
        test_calculate_lifetime_frequency_domain()
        test_calculate_lifetime_natural_frequency()
        test_calculate_lifetime_damping()
        test_calculate_weighted_average_lifetime()
        
        print("\n" + "=" * 60)
        print("✓ All lifetime calculation tests passed successfully!")
        print("=" * 60)
    except AssertionError as e:
        print(f"\n✗ Test failed: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
