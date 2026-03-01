"""
Script to predict lifetime from real acceleration data in Excel file
"""
import pandas as pd
import numpy as np
import json
from signal_processing import (
    compute_fft,
    calculate_damping_factor,
    detect_natural_frequency,
    calculate_lifetime_time_domain,
    calculate_lifetime_frequency_domain,
    calculate_lifetime_natural_frequency,
    calculate_lifetime_damping,
    calculate_weighted_average_lifetime
)
from ai_model import extract_features, load_model, predict_lifetime


def load_excel_data(filepath):
    """
    Load acceleration data from Excel file
    
    Expected format:
    - Column 1: Time (seconds) or index
    - Column 2: Acceleration (m/s²)
    
    Returns:
        time: numpy array of time values
        acceleration: numpy array of acceleration values
    """
    print(f"Loading data from {filepath}...")
    
    # Try reading the Excel file
    try:
        df = pd.read_excel(filepath)
        print(f"Excel file loaded successfully!")
        print(f"Columns found: {df.columns.tolist()}")
        print(f"Shape: {df.shape}")
        print(f"\nFirst few rows:")
        print(df.head())
        
        # Determine which columns to use
        if df.shape[1] >= 2:
            # Assume first column is time, second is acceleration
            time_col = df.columns[0]
            accel_col = df.columns[1]
            
            print(f"Using columns: '{time_col}' and '{accel_col}'")
            
            # Function to clean values with units (e.g., "4.132m" -> 4.132)
            def clean_numeric(series):
                """Remove unit suffixes like 'm', 'k', etc. and convert to float"""
                if series.dtype == 'object':
                    # Remove common unit suffixes and convert
                    cleaned = series.astype(str).str.replace(r'[a-zA-Z]+$', '', regex=True)
                    return pd.to_numeric(cleaned, errors='coerce')
                else:
                    return pd.to_numeric(series, errors='coerce')
            
            # Convert to numeric, handling unit suffixes
            time = clean_numeric(df[time_col]).values
            acceleration = clean_numeric(df[accel_col]).values
            
            print(f"Raw data preview:")
            print(f"  Time: {df[time_col].head(3).tolist()}")
            print(f"  Acceleration: {df[accel_col].head(3).tolist()}")
            
            # Check if time column looks valid
            time_valid = np.sum(~np.isnan(time)) > 0
            
            # If time column is just index, create time array
            if not time_valid or not np.all(np.diff(time[~np.isnan(time)]) > 0):
                print("Time column appears invalid or non-sequential, creating time array...")
                # Assume 1000 Hz sampling rate (adjust if needed)
                sampling_rate = 1000.0
                time = np.arange(len(acceleration)) / sampling_rate
        else:
            # Only one column - assume it's acceleration
            acceleration = pd.to_numeric(df.iloc[:, 0], errors='coerce').values
            # Create time array assuming 1000 Hz sampling rate
            sampling_rate = 1000.0
            time = np.arange(len(acceleration)) / sampling_rate
            print(f"Only one column found, assuming acceleration data")
            print(f"Created time array with {sampling_rate} Hz sampling rate")
        
        # Remove any NaN values
        valid_mask = ~(np.isnan(time) | np.isnan(acceleration))
        num_invalid = np.sum(~valid_mask)
        if num_invalid > 0:
            print(f"Removing {num_invalid} invalid/NaN values...")
        
        time = time[valid_mask]
        acceleration = acceleration[valid_mask]
        
        if len(time) == 0:
            raise ValueError("No valid data found after cleaning!")
        
        # Check if acceleration values look like they're in milli units (very small)
        max_accel = np.abs(acceleration).max()
        if max_accel < 1.0:
            print(f"⚠ Acceleration values appear to be in milli-units (max: {max_accel:.6f})")
            print(f"Converting to standard units by multiplying by 1000...")
            acceleration = acceleration * 1000.0
        
        print(f"\nData loaded successfully!")
        print(f"Time range: {time[0]:.4f} to {time[-1]:.4f} seconds")
        print(f"Acceleration range: {acceleration.min():.4f} to {acceleration.max():.4f} m/s²")
        print(f"Number of samples: {len(time)}")
        
        return time, acceleration
        
    except Exception as e:
        print(f"Error loading Excel file: {e}")
        raise


def analyze_vibration_data(time, acceleration):
    """
    Perform complete vibration analysis on the data
    
    Returns:
        dict: All computed metrics
    """
    print("\n" + "="*60)
    print("VIBRATION ANALYSIS RESULTS")
    print("="*60)
    
    results = {}
    
    # 1. Compute FFT
    print("\n1. Computing FFT...")
    frequency, amplitude = compute_fft(time, acceleration)
    results['frequency'] = frequency
    results['amplitude'] = amplitude
    print(f"   ✓ FFT computed: {len(frequency)} frequency bins")
    
    # 2. Calculate damping factor
    print("\n2. Calculating damping factor...")
    damping_factor = calculate_damping_factor(time, acceleration)
    results['damping_factor'] = damping_factor
    print(f"   ✓ Damping factor: {damping_factor:.4f}")
    
    # Interpret damping factor
    if damping_factor <= 0.10:
        damping_status = "NORMAL (low damping)"
    elif damping_factor <= 0.20:
        damping_status = "WARNING (moderate damping)"
    else:
        damping_status = "CRITICAL (high damping)"
    print(f"   Status: {damping_status}")
    
    # 3. Detect natural frequency
    print("\n3. Detecting natural frequency...")
    natural_frequency = detect_natural_frequency(frequency, amplitude)
    results['natural_frequency'] = natural_frequency
    print(f"   ✓ Natural frequency: {natural_frequency:.2f} Hz")
    
    # Check frequency shift from baseline
    baseline_freq = 50.0
    freq_shift = abs(natural_frequency - baseline_freq)
    if freq_shift > 10:
        freq_status = "CRITICAL (large shift from baseline)"
    elif freq_shift > 5:
        freq_status = "WARNING (moderate shift from baseline)"
    else:
        freq_status = "NORMAL (within baseline range)"
    print(f"   Shift from baseline (50 Hz): {freq_shift:.2f} Hz")
    print(f"   Status: {freq_status}")
    
    # 4. Calculate lifetime estimates
    print("\n4. Calculating lifetime estimates...")
    
    omega_n = 2 * np.pi * natural_frequency
    
    lifetime_time = calculate_lifetime_time_domain(
        time, acceleration, damping_factor, omega_n
    )
    results['lifetime_time'] = lifetime_time
    print(f"   ✓ Time-domain lifetime: {lifetime_time:.1f} hours")
    
    lifetime_freq = calculate_lifetime_frequency_domain(frequency, amplitude)
    results['lifetime_freq'] = lifetime_freq
    print(f"   ✓ Frequency-domain lifetime: {lifetime_freq:.1f} hours")
    
    lifetime_natural = calculate_lifetime_natural_frequency(natural_frequency)
    results['lifetime_natural'] = lifetime_natural
    print(f"   ✓ Natural frequency shift lifetime: {lifetime_natural:.1f} hours")
    
    lifetime_damping = calculate_lifetime_damping(damping_factor)
    results['lifetime_damping'] = lifetime_damping
    print(f"   ✓ Damping-based lifetime: {lifetime_damping:.1f} hours")
    
    # 5. Calculate weighted average
    print("\n5. Calculating weighted average lifetime...")
    average_lifetime = calculate_weighted_average_lifetime(
        lifetime_time, lifetime_freq, lifetime_natural, lifetime_damping
    )
    results['average_lifetime'] = average_lifetime
    print(f"   ✓ Weighted average lifetime: {average_lifetime:.1f} hours")
    
    # 6. AI prediction
    print("\n6. AI model prediction...")
    try:
        model = load_model()
        ai_lifetime = predict_lifetime(
            model, acceleration, damping_factor, natural_frequency, amplitude
        )
        results['ai_lifetime'] = ai_lifetime
        print(f"   ✓ AI predicted lifetime: {ai_lifetime:.1f} hours")
        
        # Compare AI with average
        percent_diff = abs(ai_lifetime - average_lifetime) / average_lifetime * 100
        print(f"   Difference from average: {percent_diff:.1f}%")
        
        if percent_diff < 10:
            agreement = "GOOD AGREEMENT"
        elif percent_diff < 20:
            agreement = "MODERATE AGREEMENT"
        else:
            agreement = "SIGNIFICANT DIVERGENCE"
        print(f"   Status: {agreement}")
        
    except Exception as e:
        print(f"   ⚠ AI prediction failed: {e}")
        print(f"   Using average lifetime as fallback")
        results['ai_lifetime'] = average_lifetime
    
    return results


def save_results(results, output_file='analysis_results.json'):
    """Save analysis results to JSON file"""
    # Convert numpy arrays to lists for JSON serialization
    results_serializable = {}
    for key, value in results.items():
        if isinstance(value, np.ndarray):
            results_serializable[key] = value.tolist()
        elif isinstance(value, (np.float64, np.float32)):
            results_serializable[key] = float(value)
        else:
            results_serializable[key] = value
    
    with open(output_file, 'w') as f:
        json.dump(results_serializable, f, indent=2)
    
    print(f"\n✓ Results saved to {output_file}")


def main():
    """Main execution function"""
    # Path to your Excel file
    excel_file = "../acceleration data_669853.tmp.xlsx"
    
    try:
        # Load data from Excel
        time, acceleration = load_excel_data(excel_file)
        
        # Perform analysis
        results = analyze_vibration_data(time, acceleration)
        
        # Save results
        save_results(results, 'real_data_analysis_results.json')
        
        # Print summary
        print("\n" + "="*60)
        print("SUMMARY")
        print("="*60)
        print(f"Damping Factor:        {results['damping_factor']:.4f}")
        print(f"Natural Frequency:     {results['natural_frequency']:.2f} Hz")
        print(f"Time-Domain Lifetime:  {results['lifetime_time']:.1f} hours")
        print(f"Freq-Domain Lifetime:  {results['lifetime_freq']:.1f} hours")
        print(f"Natural Freq Lifetime: {results['lifetime_natural']:.1f} hours")
        print(f"Damping Lifetime:      {results['lifetime_damping']:.1f} hours")
        print(f"Average Lifetime:      {results['average_lifetime']:.1f} hours")
        print(f"AI Predicted Lifetime: {results['ai_lifetime']:.1f} hours")
        print("="*60)
        
        # Convert to days for easier interpretation
        print(f"\nLifetime in days: {results['average_lifetime']/24:.1f} days")
        print(f"AI prediction in days: {results['ai_lifetime']/24:.1f} days")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
