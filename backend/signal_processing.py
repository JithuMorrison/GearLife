# Signal processing module for vibration analysis
# This module contains FFT, damping factor, natural frequency detection,
# and lifetime calculation functions

import numpy as np
from scipy.signal import find_peaks

# Placeholder functions - to be implemented

def compute_fft(time: np.ndarray, acceleration: np.ndarray):
    """
    Compute Fast Fourier Transform
    
    Returns:
        frequency: Frequency array (Hz)
        amplitude: Amplitude spectrum
    """
    # Handle edge cases: empty arrays
    if len(acceleration) == 0 or len(time) == 0:
        return np.array([]), np.array([])
    
    # Handle edge case: single-element arrays
    if len(acceleration) == 1:
        return np.array([0.0]), np.array([np.abs(acceleration[0])])
    
    # Compute sampling interval
    n = len(acceleration)
    dt = time[1] - time[0]  # Sampling interval
    
    # Compute FFT using numpy's real FFT for real-valued signals
    freq = np.fft.rfftfreq(n, dt)
    fft_values = np.fft.rfft(acceleration)
    amplitude = np.abs(fft_values)
    
    return freq, amplitude

def calculate_damping_factor(time: np.ndarray, acceleration: np.ndarray) -> float:
    """
    Calculate damping factor using logarithmic decrement
    
    Returns:
        zeta: Damping factor (dimensionless)
    """
    # Handle edge cases: empty or insufficient data
    if len(acceleration) < 2:
        return 0.05  # Default damping for underdamped systems
    
    # Find local maxima (peaks) in acceleration signal
    peaks, _ = find_peaks(np.abs(acceleration))
    
    # Need at least 2 peaks for logarithmic decrement
    if len(peaks) < 2:
        return 0.05  # Default damping for underdamped systems
    
    # Get first two peak amplitudes
    x1 = np.abs(acceleration[peaks[0]])
    x2 = np.abs(acceleration[peaks[1]])
    
    # Handle edge cases: zero amplitude or non-decaying signal
    if x2 == 0 or x1 <= x2:
        return 0.05
    
    # Compute logarithmic decrement: delta = ln(x1/x2)
    delta = np.log(x1 / x2)
    
    # Calculate damping ratio: zeta = delta / sqrt(4π² + delta²)
    zeta = delta / np.sqrt(4 * np.pi**2 + delta**2)
    
    return zeta

def detect_natural_frequency(frequency: np.ndarray, amplitude: np.ndarray) -> float:
    """
    Detect natural frequency as peak in amplitude spectrum
    
    Returns:
        natural_freq: Natural frequency (Hz)
    """
    # Handle edge cases: empty arrays
    if len(amplitude) == 0 or len(frequency) == 0:
        return 0.0
    
    # Exclude DC component (first element at index 0)
    if len(amplitude) < 2:
        return 0.0
    
    # Find peak in amplitude spectrum (excluding DC component)
    peak_idx = np.argmax(amplitude[1:]) + 1
    
    return frequency[peak_idx]

def calculate_lifetime_time_domain(
    time: np.ndarray,
    acceleration: np.ndarray,
    zeta: float,
    omega_n: float,
    threshold: float = 0.01
) -> float:
    """
    Calculate lifetime from exponential decay envelope
    
    Model: A(t) = A0 * exp(-zeta * omega_n * t)
    
    Returns:
        lifetime: Estimated time until amplitude < threshold (hours)
    """
    # Handle edge cases: empty data or invalid parameters
    if len(acceleration) == 0 or omega_n == 0:
        return 1000.0  # Default high lifetime
    
    # Get initial amplitude (maximum absolute value)
    A0 = np.max(np.abs(acceleration))
    if A0 == 0:
        return 1000.0
    
    # Solve for t when A(t) = threshold * A0
    # threshold * A0 = A0 * exp(-zeta * omega_n * t)
    # threshold = exp(-zeta * omega_n * t)
    # ln(threshold) = -zeta * omega_n * t
    # t = -ln(threshold) / (zeta * omega_n)
    
    decay_rate = zeta * omega_n
    if decay_rate <= 0:
        return 1000.0
    
    lifetime_seconds = -np.log(threshold) / decay_rate
    lifetime_hours = lifetime_seconds / 3600.0
    
    # Cap at reasonable bounds (10-10000 hours)
    return min(max(lifetime_hours, 10.0), 10000.0)

def calculate_lifetime_frequency_domain(
    frequency: np.ndarray,
    amplitude: np.ndarray,
    energy_threshold: float = 100.0
) -> float:
    """
    Calculate lifetime from spectral energy
    
    Higher energy indicates more vibration → shorter lifetime
    
    Returns:
        lifetime: Estimated lifetime (hours)
    """
    # Handle edge cases: empty arrays
    if len(amplitude) == 0:
        return 1000.0
    
    # Compute spectral energy: E = sum(A(f)²)
    spectral_energy = np.sum(amplitude**2)
    
    if spectral_energy == 0:
        return 1000.0
    
    # Inverse relationship: lifetime ∝ 1/energy
    lifetime_hours = energy_threshold / spectral_energy * 1000.0
    
    # Clamp to reasonable range (10-10000 hours)
    return min(max(lifetime_hours, 10.0), 10000.0)

def calculate_lifetime_natural_frequency(
    natural_freq: float,
    baseline_freq: float = 50.0,
    sensitivity: float = 1000.0
) -> float:
    """
    Calculate lifetime from natural frequency shift
    
    Frequency shift indicates structural changes → reduced lifetime
    
    Returns:
        lifetime: Estimated lifetime (hours)
    """
    # Handle edge case: invalid frequency
    if natural_freq == 0:
        return 1000.0
    
    # Calculate frequency shift from baseline
    freq_shift = abs(natural_freq - baseline_freq)
    
    # If minimal shift, return maximum lifetime
    if freq_shift < 0.1:
        return 10000.0
    
    # Inverse relationship: lifetime ∝ 1/|shift|
    lifetime_hours = sensitivity / freq_shift
    
    # Clamp to reasonable range (10-10000 hours)
    return min(max(lifetime_hours, 10.0), 10000.0)

def calculate_lifetime_damping(
    zeta: float,
    baseline_damping: float = 0.05,
    sensitivity: float = 100.0
) -> float:
    """
    Calculate lifetime from damping factor
    
    Higher damping indicates wear → shorter lifetime
    
    Returns:
        lifetime: Estimated lifetime (hours)
    """
    # Handle edge case: invalid damping
    if zeta <= 0:
        return 1000.0
    
    # Calculate damping increase from baseline
    damping_increase = max(zeta - baseline_damping, 0.001)
    
    # Inverse relationship: lifetime ∝ 1/damping_increase
    lifetime_hours = sensitivity / damping_increase
    
    # Clamp to reasonable range (10-10000 hours)
    return min(max(lifetime_hours, 10.0), 10000.0)

def calculate_weighted_average_lifetime(
    lifetime_time: float,
    lifetime_freq: float,
    lifetime_natural: float,
    lifetime_damping: float
) -> float:
    """
    Calculate weighted average of all lifetime estimates
    
    Formula: L_avg = 0.25 * (L_time + L_freq + L_natural + L_damping)
    
    Returns:
        average_lifetime: Weighted average (hours)
    """
    # Ensure all four components are available (non-zero)
    if lifetime_time == 0 or lifetime_freq == 0 or lifetime_natural == 0 or lifetime_damping == 0:
        return 0.0
    
    # Calculate weighted average with equal weights (0.25 each)
    average_lifetime = 0.25 * lifetime_time + 0.25 * lifetime_freq + \
                      0.25 * lifetime_natural + 0.25 * lifetime_damping
    
    return average_lifetime
