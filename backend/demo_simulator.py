#!/usr/bin/env python3
"""
Demo script for the vibration simulator

This script demonstrates the simulator functionality without requiring
the backend server to be running. It shows:
1. Signal generation with different parameters
2. Visualization of the damped oscillation
3. Data format that would be sent to the backend
"""

import numpy as np
import matplotlib.pyplot as plt
from simulator import generate_vibration_signal

def demo_signal_generation():
    """Demonstrate signal generation with various parameters"""
    
    print("=" * 60)
    print("Vibration Simulator Demo")
    print("=" * 60)
    print()
    
    # Demo 1: Standard signal
    print("Demo 1: Standard damped oscillation")
    print("-" * 60)
    time1, accel1 = generate_vibration_signal(
        duration=2.0,
        sampling_rate=1000.0,
        amplitude=10.0,
        frequency=50.0,
        damping=0.05
    )
    print(f"Duration: 2.0s")
    print(f"Samples: {len(time1)}")
    print(f"Amplitude: 10.0 m/s²")
    print(f"Frequency: 50.0 Hz")
    print(f"Damping: 0.05")
    print(f"Max acceleration: {np.max(np.abs(accel1)):.3f} m/s²")
    print()
    
    # Demo 2: High damping
    print("Demo 2: High damping (faster decay)")
    print("-" * 60)
    time2, accel2 = generate_vibration_signal(
        duration=2.0,
        sampling_rate=1000.0,
        amplitude=10.0,
        frequency=50.0,
        damping=0.15  # Higher damping
    )
    print(f"Duration: 2.0s")
    print(f"Damping: 0.15 (3x higher)")
    print(f"Max acceleration: {np.max(np.abs(accel2)):.3f} m/s²")
    print()
    
    # Demo 3: High frequency
    print("Demo 3: High frequency oscillation")
    print("-" * 60)
    time3, accel3 = generate_vibration_signal(
        duration=2.0,
        sampling_rate=1000.0,
        amplitude=10.0,
        frequency=100.0,  # Higher frequency
        damping=0.05
    )
    print(f"Duration: 2.0s")
    print(f"Frequency: 100.0 Hz (2x higher)")
    print(f"Max acceleration: {np.max(np.abs(accel3)):.3f} m/s²")
    print()
    
    # Demo 4: Data format for backend
    print("Demo 4: Data format for backend API")
    print("-" * 60)
    time4, accel4 = generate_vibration_signal(
        duration=0.5,
        sampling_rate=500.0,
        amplitude=10.0,
        frequency=50.0,
        damping=0.05
    )
    payload = {
        "time": time4.tolist(),
        "acceleration": accel4.tolist()
    }
    print(f"Payload structure:")
    print(f"  'time': list of {len(payload['time'])} floats")
    print(f"  'acceleration': list of {len(payload['acceleration'])} floats")
    print(f"Sample data (first 5 points):")
    for i in range(5):
        print(f"  t={payload['time'][i]:.6f}s, a={payload['acceleration'][i]:.6f} m/s²")
    print()
    
    # Create visualization
    print("Creating visualization...")
    fig, axes = plt.subplots(2, 2, figsize=(12, 8))
    fig.suptitle('Vibration Simulator Demo', fontsize=16, fontweight='bold')
    
    # Plot 1: Standard signal
    axes[0, 0].plot(time1, accel1, 'b-', linewidth=0.5)
    axes[0, 0].set_title('Standard Damping (ζ=0.05)')
    axes[0, 0].set_xlabel('Time (s)')
    axes[0, 0].set_ylabel('Acceleration (m/s²)')
    axes[0, 0].grid(True, alpha=0.3)
    
    # Plot 2: High damping
    axes[0, 1].plot(time2, accel2, 'r-', linewidth=0.5)
    axes[0, 1].set_title('High Damping (ζ=0.15)')
    axes[0, 1].set_xlabel('Time (s)')
    axes[0, 1].set_ylabel('Acceleration (m/s²)')
    axes[0, 1].grid(True, alpha=0.3)
    
    # Plot 3: High frequency
    axes[1, 0].plot(time3[:500], accel3[:500], 'g-', linewidth=0.5)
    axes[1, 0].set_title('High Frequency (100 Hz, first 0.5s)')
    axes[1, 0].set_xlabel('Time (s)')
    axes[1, 0].set_ylabel('Acceleration (m/s²)')
    axes[1, 0].grid(True, alpha=0.3)
    
    # Plot 4: Comparison of decay rates
    axes[1, 1].plot(time1, np.abs(accel1), 'b-', label='ζ=0.05', linewidth=1)
    axes[1, 1].plot(time2, np.abs(accel2), 'r-', label='ζ=0.15', linewidth=1)
    axes[1, 1].set_title('Amplitude Decay Comparison')
    axes[1, 1].set_xlabel('Time (s)')
    axes[1, 1].set_ylabel('|Acceleration| (m/s²)')
    axes[1, 1].legend()
    axes[1, 1].grid(True, alpha=0.3)
    axes[1, 1].set_yscale('log')
    
    plt.tight_layout()
    
    # Try to save the plot
    try:
        plt.savefig('simulator_demo.png', dpi=150, bbox_inches='tight')
        print("✓ Visualization saved to: simulator_demo.png")
    except Exception as e:
        print(f"Could not save visualization: {e}")
    
    # Try to show the plot
    try:
        plt.show()
    except Exception as e:
        print(f"Could not display visualization: {e}")
    
    print()
    print("=" * 60)
    print("Demo complete!")
    print("=" * 60)

if __name__ == "__main__":
    try:
        demo_signal_generation()
    except ImportError as e:
        print(f"Error: Missing dependency - {e}")
        print("Note: matplotlib is required for visualization")
        print("Install with: pip install matplotlib")
    except Exception as e:
        print(f"Error: {e}")
