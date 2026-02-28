# Vibration Data Simulator Usage Guide

## Overview

The vibration data simulator (`simulator.py`) generates synthetic vibration data for testing the Vibration Lifetime Prediction Platform. It simulates damped oscillations using the formula:

```
x(t) = A * exp(-zeta * omega * t) * sin(omega * t) + noise
```

## Features

- Generates realistic damped sinusoidal vibration signals
- Configurable amplitude, frequency, and damping parameters
- Continuous data streaming to backend at regular intervals
- Automatic error handling and retry logic

## Usage

### 1. Start the Backend Server

First, make sure the backend server is running:

```bash
cd backend
python app.py
```

The server should start on `http://localhost:8000`

### 2. Run the Simulator

In a separate terminal, run the simulator:

```bash
cd backend
python simulator.py
```

The simulator will start sending data to the backend every 2 seconds.

### 3. Customize Parameters

You can customize the simulator parameters by editing the `__main__` section in `simulator.py`:

```python
asyncio.run(run_simulator(
    backend_url="http://localhost:8000",  # Backend URL
    interval=2.0,                          # Time between transmissions (seconds)
    duration=1.0,                          # Duration of each signal chunk (seconds)
    sampling_rate=1000.0,                  # Samples per second
    amplitude=10.0,                        # Signal amplitude (m/s²)
    frequency=50.0,                        # Oscillation frequency (Hz)
    damping=0.05                           # Damping factor (dimensionless)
))
```

### 4. Stop the Simulator

Press `Ctrl+C` to stop the simulator.

## API Reference

### `generate_vibration_signal()`

Generates a single vibration signal chunk.

**Parameters:**

- `duration` (float): Signal duration in seconds (default: 1.0)
- `sampling_rate` (float): Samples per second (default: 1000.0)
- `amplitude` (float): Signal amplitude in m/s² (default: 10.0)
- `frequency` (float): Oscillation frequency in Hz (default: 50.0)
- `damping` (float): Damping factor, dimensionless (default: 0.05)

**Returns:**

- `tuple`: (time, acceleration) where both are numpy arrays

**Example:**

```python
from simulator import generate_vibration_signal

time, acceleration = generate_vibration_signal(
    duration=2.0,
    sampling_rate=1000.0,
    amplitude=15.0,
    frequency=60.0,
    damping=0.08
)
```

### `run_simulator()`

Continuously generates and sends vibration data to the backend.

**Parameters:**

- `backend_url` (str): Base URL of the backend API (default: "http://localhost:8000")
- `interval` (float): Time between transmissions in seconds (default: 2.0)
- `duration` (float): Duration of each signal chunk in seconds (default: 1.0)
- `sampling_rate` (float): Samples per second (default: 1000.0)
- `amplitude` (float): Signal amplitude in m/s² (default: 10.0)
- `frequency` (float): Oscillation frequency in Hz (default: 50.0)
- `damping` (float): Damping factor (default: 0.05)

**Example:**

```python
import asyncio
from simulator import run_simulator

asyncio.run(run_simulator(
    backend_url="http://localhost:8000",
    interval=1.0,  # Send data every second
    amplitude=20.0,  # Higher amplitude
    frequency=100.0  # Higher frequency
))
```

## Testing

### Unit Tests

Test the signal generation function:

```bash
cd backend
python test_simulator.py
```

This will verify:

- Signal generation produces correct array lengths
- Time and acceleration arrays match
- Damping effect is present (amplitude decays over time)
- Output types are correct (numpy arrays)

### Integration Tests

Test the simulator's connection to the backend:

```bash
cd backend
# Make sure backend is running first!
python test_simulator_integration.py
```

This will verify:

- Simulator can connect to the backend
- Data is successfully transmitted
- Backend accepts and processes the data

## Troubleshooting

### "Connection failed: Backend server is not running"

Make sure the backend server is running on port 8000:

```bash
cd backend
python app.py
```

### "Network error" or timeout

Check that:

1. The backend server is running
2. The `backend_url` parameter is correct
3. No firewall is blocking port 8000

### Simulator stops unexpectedly

Check the console output for error messages. Common issues:

- Backend server crashed or stopped
- Network connectivity issues
- Invalid parameters (e.g., negative values)

## Requirements Validation

The simulator implementation satisfies the following requirements:

- **Requirement 13.1**: Generates signals using damped oscillation formula
- **Requirement 13.2**: Sends periodic data chunks to /send-data endpoint
- **Requirement 13.3**: Simulates realistic damping and frequency parameters
- **Requirement 13.4**: Generates time and acceleration arrays in required JSON format
- **Requirement 13.5**: Allows configuration of simulation parameters

## Example Output

When running, the simulator produces output like:

```
Starting vibration simulator...
Backend URL: http://localhost:8000
Interval: 2.0s, Duration: 1.0s
Parameters: amplitude=10.0, frequency=50.0Hz, damping=0.05
Press Ctrl+C to stop

[1] Data sent successfully: Data received and processed
[2] Data sent successfully: Data received and processed
[3] Data sent successfully: Data received and processed
...
```
