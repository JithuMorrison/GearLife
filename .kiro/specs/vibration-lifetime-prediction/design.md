# Design Document: Vibration Lifetime Prediction Platform

## Overview

The Mechanical System Lifetime Prediction Platform is a full-stack web application that performs real-time vibration analysis and AI-based predictive maintenance. The system receives acceleration time-series data, processes it through multiple signal processing algorithms, computes lifetime estimates using both traditional engineering methods and machine learning, and presents all metrics through a professional industrial-themed dashboard.

The architecture follows a client-server model with a Python FastAPI backend handling all computation and a JavaScript frontend providing real-time visualization. Data flows unidirectionally from sensors (or simulator) → backend processing → JSON storage → frontend display, with polling-based updates ensuring real-time responsiveness.

## Architecture

### System Components

```
┌─────────────┐
│  Simulator  │ (Optional - for testing)
└──────┬──────┘
       │ POST /send-data
       ▼
┌─────────────────────────────────────────┐
│           Backend (FastAPI)              │
│  ┌────────────────────────────────────┐ │
│  │  API Layer (app.py)                │ │
│  │  - /send-data                      │ │
│  │  - /get-data                       │ │
│  │  - /full-refresh                   │ │
│  └────────┬───────────────────────────┘ │
│           │                              │
│  ┌────────▼───────────────────────────┐ │
│  │  Signal Processing                 │ │
│  │  (signal_processing.py)            │ │
│  │  - FFT computation                 │ │
│  │  - Damping factor calculation      │ │
│  │  - Natural frequency detection     │ │
│  │  - Lifetime calculations (4 types) │ │
│  └────────┬───────────────────────────┘ │
│           │                              │
│  ┌────────▼───────────────────────────┐ │
│  │  AI Model (ai_model.py)            │ │
│  │  - Feature extraction              │ │
│  │  - Regression prediction           │ │
│  └────────┬───────────────────────────┘ │
│           │                              │
│  ┌────────▼───────────────────────────┐ │
│  │  Data Store (data_store.json)      │ │
│  │  - Persistent storage              │ │
│  │  - State management                │ │
│  └────────────────────────────────────┘ │
└─────────────┬───────────────────────────┘
              │ GET /get-data (poll every 2s)
              ▼
┌─────────────────────────────────────────┐
│         Frontend (HTML/CSS/JS)          │
│  ┌────────────────────────────────────┐ │
│  │  Visualization Layer               │ │
│  │  - Time-domain chart               │ │
│  │  - Frequency-domain chart          │ │
│  │  - Metrics dashboard               │ │
│  │  - Comparison panels               │ │
│  └────────────────────────────────────┘ │
└─────────────────────────────────────────┘
```

### Technology Stack

**Backend:**

- FastAPI: Async web framework for high-performance API endpoints
- NumPy: Numerical computing for array operations
- SciPy: Scientific computing for FFT and signal processing
- scikit-learn: Machine learning for AI lifetime prediction
- Python 3.8+: Runtime environment

**Frontend:**

- Vanilla JavaScript: Real-time data fetching and DOM updates
- HTML5 Canvas or Chart.js: High-performance charting
- CSS3: Industrial-themed styling with animations

**Data Storage:**

- JSON file: Simple, human-readable persistent storage

### Communication Protocol

- REST API with JSON payloads
- Polling-based updates (2-second interval)
- Stateful backend with new_data_available flag for efficient updates

## Components and Interfaces

### Backend Components

#### 1. API Layer (app.py)

**Responsibilities:**

- Handle HTTP requests and responses
- Coordinate between signal processing, AI model, and data storage
- Manage concurrent access to data_store.json

**Endpoints:**

```python
POST /send-data
Input: {
  "time": [float],        # Time values in seconds
  "acceleration": [float] # Acceleration values in m/s²
}
Output: {
  "status": "success",
  "message": "Data received and processed"
}
```

```python
GET /get-data
Output: {
  "new_data_available": bool,
  "time": [float],              # Only new data if available
  "acceleration": [float],      # Only new data if available
  "frequency": [float],
  "amplitude": [float],
  "damping_factor": float,
  "natural_frequency": float,
  "lifetime_time": float,
  "lifetime_freq": float,
  "lifetime_natural": float,
  "lifetime_damping": float,
  "average_lifetime": float,
  "ai_lifetime": float
}
```

```python
GET /full-refresh
Output: {
  # Complete dataset - all arrays and metrics
  "time": [float],
  "acceleration": [float],
  "frequency": [float],
  "amplitude": [float],
  "damping_factor": float,
  "natural_frequency": float,
  "lifetime_time": float,
  "lifetime_freq": float,
  "lifetime_natural": float,
  "lifetime_damping": float,
  "average_lifetime": float,
  "ai_lifetime": float
}
```

**Key Functions:**

```python
async def append_data(new_time: list, new_acceleration: list) -> None:
    """Append new data to data_store.json and trigger processing"""

async def trigger_processing() -> None:
    """Orchestrate signal processing and AI prediction pipeline"""

async def load_data_store() -> dict:
    """Load current state from JSON file"""

async def save_data_store(data: dict) -> None:
    """Save updated state to JSON file"""
```

#### 2. Signal Processing Module (signal_processing.py)

**Responsibilities:**

- Perform FFT conversion
- Calculate damping factor using logarithmic decrement
- Detect natural frequency from spectrum
- Compute four types of lifetime estimates

**Key Functions:**

```python
def compute_fft(time: np.ndarray, acceleration: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """
    Compute Fast Fourier Transform

    Returns:
        frequency: Frequency array (Hz)
        amplitude: Amplitude spectrum
    """
    n = len(acceleration)
    dt = time[1] - time[0]  # Sampling interval
    freq = np.fft.rfftfreq(n, dt)
    fft_values = np.fft.rfft(acceleration)
    amplitude = np.abs(fft_values)
    return freq, amplitude

def calculate_damping_factor(time: np.ndarray, acceleration: np.ndarray) -> float:
    """
    Calculate damping factor using logarithmic decrement

    Algorithm:
    1. Find local maxima (peaks) in acceleration signal
    2. Compute logarithmic decrement: delta = ln(x1/x2)
    3. Calculate damping ratio: zeta = delta / sqrt(4π² + delta²)

    Returns:
        zeta: Damping factor (dimensionless)
    """
    from scipy.signal import find_peaks

    peaks, _ = find_peaks(np.abs(acceleration))
    if len(peaks) < 2:
        return 0.05  # Default damping for underdamped systems

    x1 = np.abs(acceleration[peaks[0]])
    x2 = np.abs(acceleration[peaks[1]])

    if x2 == 0 or x1 <= x2:
        return 0.05

    delta = np.log(x1 / x2)
    zeta = delta / np.sqrt(4 * np.pi**2 + delta**2)
    return zeta

def detect_natural_frequency(frequency: np.ndarray, amplitude: np.ndarray) -> float:
    """
    Detect natural frequency as peak in amplitude spectrum

    Returns:
        natural_freq: Natural frequency (Hz)
    """
    # Exclude DC component (first element)
    if len(amplitude) < 2:
        return 0.0

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
    if len(acceleration) == 0 or omega_n == 0:
        return 1000.0  # Default high lifetime

    A0 = np.max(np.abs(acceleration))
    if A0 == 0:
        return 1000.0

    # Solve for t when A(t) = threshold * A0
    # threshold * A0 = A0 * exp(-zeta * omega_n * t)
    # ln(threshold) = -zeta * omega_n * t
    # t = -ln(threshold) / (zeta * omega_n)

    decay_rate = zeta * omega_n
    if decay_rate <= 0:
        return 1000.0

    lifetime_seconds = -np.log(threshold) / decay_rate
    lifetime_hours = lifetime_seconds / 3600.0
    return min(lifetime_hours, 10000.0)  # Cap at reasonable maximum

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
    if len(amplitude) == 0:
        return 1000.0

    spectral_energy = np.sum(amplitude**2)

    if spectral_energy == 0:
        return 1000.0

    # Inverse relationship: lifetime ∝ 1/energy
    lifetime_hours = energy_threshold / spectral_energy * 1000.0
    return min(max(lifetime_hours, 10.0), 10000.0)  # Clamp to reasonable range

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
    if natural_freq == 0:
        return 1000.0

    freq_shift = abs(natural_freq - baseline_freq)

    if freq_shift < 0.1:  # Minimal shift
        return 10000.0

    # Inverse relationship: lifetime ∝ 1/|shift|
    lifetime_hours = sensitivity / freq_shift
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
    if zeta <= 0:
        return 1000.0

    damping_increase = max(zeta - baseline_damping, 0.001)

    # Inverse relationship: lifetime ∝ 1/damping_increase
    lifetime_hours = sensitivity / damping_increase
    return min(max(lifetime_hours, 10.0), 10000.0)

def calculate_weighted_average_lifetime(
    lifetime_time: float,
    lifetime_freq: float,
    lifetime_natural: float,
    lifetime_damping: float
) -> float:
    """
    Calculate weighted average of all lifetime estimates

    Returns:
        average_lifetime: Weighted average (hours)
    """
    return 0.25 * lifetime_time + 0.25 * lifetime_freq + \
           0.25 * lifetime_natural + 0.25 * lifetime_damping
```

#### 3. AI Model Module (ai_model.py)

**Responsibilities:**

- Extract features from processed data
- Predict lifetime using trained regression model
- Handle model training and persistence

**Key Functions:**

```python
def extract_features(
    acceleration: np.ndarray,
    damping_factor: float,
    natural_frequency: float,
    amplitude: np.ndarray
) -> np.ndarray:
    """
    Extract features for AI model

    Features:
    1. RMS acceleration
    2. Peak acceleration
    3. Damping factor
    4. Natural frequency
    5. Spectral energy

    Returns:
        features: Feature vector (5 elements)
    """
    rms_accel = np.sqrt(np.mean(acceleration**2))
    peak_accel = np.max(np.abs(acceleration))
    spectral_energy = np.sum(amplitude**2)

    return np.array([
        rms_accel,
        peak_accel,
        damping_factor,
        natural_frequency,
        spectral_energy
    ])

def train_model(training_data: list[dict]) -> object:
    """
    Train regression model on historical data

    Model: RandomForestRegressor or MLPRegressor

    Returns:
        model: Trained scikit-learn model
    """
    from sklearn.ensemble import RandomForestRegressor

    X = []  # Features
    y = []  # Target lifetimes

    for sample in training_data:
        features = extract_features(
            sample['acceleration'],
            sample['damping_factor'],
            sample['natural_frequency'],
            sample['amplitude']
        )
        X.append(features)
        y.append(sample['actual_lifetime'])

    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X, y)
    return model

def predict_lifetime(
    model: object,
    acceleration: np.ndarray,
    damping_factor: float,
    natural_frequency: float,
    amplitude: np.ndarray
) -> float:
    """
    Predict lifetime using trained AI model

    Returns:
        ai_lifetime: Predicted lifetime (hours)
    """
    features = extract_features(
        acceleration,
        damping_factor,
        natural_frequency,
        amplitude
    )

    prediction = model.predict([features])[0]
    return max(prediction, 0.0)  # Ensure non-negative
```

#### 4. Simulator Module (simulator.py)

**Responsibilities:**

- Generate synthetic vibration data for testing
- Simulate realistic damped oscillations
- Send data to backend at regular intervals

**Key Functions:**

```python
def generate_vibration_signal(
    duration: float = 1.0,
    sampling_rate: float = 1000.0,
    amplitude: float = 10.0,
    frequency: float = 50.0,
    damping: float = 0.05
) -> tuple[np.ndarray, np.ndarray]:
    """
    Generate damped sinusoidal vibration signal

    Model: x(t) = A * exp(-zeta * omega * t) * sin(omega * t)

    Returns:
        time: Time array (seconds)
        acceleration: Acceleration array (m/s²)
    """
    t = np.linspace(0, duration, int(duration * sampling_rate))
    omega = 2 * np.pi * frequency

    # Damped oscillation
    envelope = amplitude * np.exp(-damping * omega * t)
    signal = envelope * np.sin(omega * t)

    # Add small noise for realism
    noise = np.random.normal(0, amplitude * 0.01, len(t))
    acceleration = signal + noise

    return t, acceleration

async def run_simulator(
    backend_url: str = "http://localhost:8000",
    interval: float = 2.0
):
    """
    Continuously generate and send vibration data

    Sends data chunks every 'interval' seconds
    """
    import aiohttp

    async with aiohttp.ClientSession() as session:
        while True:
            time, acceleration = generate_vibration_signal()

            payload = {
                "time": time.tolist(),
                "acceleration": acceleration.tolist()
            }

            await session.post(f"{backend_url}/send-data", json=payload)
            await asyncio.sleep(interval)
```

### Frontend Components

#### 1. Data Fetching Layer (script.js)

**Responsibilities:**

- Poll backend for updates
- Manage application state
- Update visualizations

**Key Functions:**

```javascript
async function pollData() {
  try {
    const response = await fetch("/get-data");
    const data = await response.json();

    if (data.new_data_available) {
      updateCharts(data);
      updateMetrics(data);
    }
  } catch (error) {
    console.error("Failed to fetch data:", error);
  }
}

async function fullRefresh() {
  try {
    const response = await fetch("/full-refresh");
    const data = await response.json();

    initializeCharts(data);
    updateMetrics(data);
  } catch (error) {
    console.error("Failed to refresh data:", error);
  }
}

// Poll every 2 seconds
setInterval(pollData, 2000);

// Full refresh on page load
window.addEventListener("load", fullRefresh);
```

#### 2. Visualization Layer

**Time-Domain Chart:**

- Line chart showing acceleration vs time
- Incremental updates for real-time feel
- Axis labels: "Time (s)" and "Acceleration (m/s²)"

**Frequency-Domain Chart:**

- Line chart showing amplitude vs frequency
- Highlight natural frequency peak
- Axis labels: "Frequency (Hz)" and "Amplitude"

**Metrics Dashboard:**

- Numeric displays for all computed values
- Circular gauges for damping factor
- Color-coded indicators for lifetime estimates

**Comparison Panel:**

- Side-by-side display of average vs AI lifetime
- Percentage difference calculation
- Visual indicators (green = agreement, red = divergence)

## Data Models

### Data Store Schema (data_store.json)

```json
{
  "time": [], // Array of time values (seconds)
  "acceleration": [], // Array of acceleration values (m/s²)
  "frequency": [], // Array of frequency values (Hz)
  "amplitude": [], // Array of FFT amplitude values
  "damping_factor": 0.0, // Damping ratio (dimensionless)
  "natural_frequency": 0.0, // Natural frequency (Hz)
  "lifetime_time": 0.0, // Time-domain lifetime (hours)
  "lifetime_freq": 0.0, // Frequency-domain lifetime (hours)
  "lifetime_natural": 0.0, // Natural frequency shift lifetime (hours)
  "lifetime_damping": 0.0, // Damping-based lifetime (hours)
  "average_lifetime": 0.0, // Weighted average lifetime (hours)
  "ai_lifetime": 0.0, // AI predicted lifetime (hours)
  "new_data_available": false // Flag for incremental updates
}
```

### API Request/Response Models

**SendDataRequest:**

```typescript
{
  time: number[],          // Time values in seconds
  acceleration: number[]   // Acceleration values in m/s²
}
```

**GetDataResponse:**

```typescript
{
  new_data_available: boolean,
  time?: number[],              // Only if new data available
  acceleration?: number[],      // Only if new data available
  frequency: number[],
  amplitude: number[],
  damping_factor: number,
  natural_frequency: number,
  lifetime_time: number,
  lifetime_freq: number,
  lifetime_natural: number,
  lifetime_damping: number,
  average_lifetime: number,
  ai_lifetime: number
}
```

## Correctness Properties

A property is a characteristic or behavior that should hold true across all valid executions of a system—essentially, a formal statement about what the system should do. Properties serve as the bridge between human-readable specifications and machine-verifiable correctness guarantees.

### Backend Data Ingestion Properties

**Property 1: Data format acceptance**
_For any_ valid time and acceleration arrays, when sent to the /send-data endpoint, the Backend should accept the data without error and return a success response.
**Validates: Requirements 1.1**

**Property 2: Data append behavior**
_For any_ existing data store and new data chunk, when new data is received, the Backend should append the new data such that the total length equals the sum of previous length and new data length.
**Validates: Requirements 1.2, 2.3**

**Property 3: New data flag setting**
_For any_ data submission, when new data is appended to the store, the new_data_available flag should be set to true.
**Validates: Requirements 1.3**

**Property 4: Processing trigger**
_For any_ data submission, when data is received, all signal processing metrics (FFT, damping, natural frequency, lifetimes) should be recalculated and updated in the data store.
**Validates: Requirements 1.5**

### Backend Signal Processing Properties

**Property 5: FFT computation**
_For any_ time-domain acceleration signal, when FFT is performed, the Backend should produce frequency and amplitude arrays where frequency values are non-negative and monotonically increasing.
**Validates: Requirements 3.1, 3.2**

**Property 6: FFT amplitude non-negativity**
_For any_ FFT computation, all amplitude values should be non-negative (amplitude >= 0).
**Validates: Requirements 3.3**

**Property 7: FFT array length consistency**
_For any_ FFT computation, the frequency and amplitude arrays should have the same length.
**Validates: Requirements 3.3, 3.4**

**Property 8: Damping factor calculation**
_For any_ signal with detectable peaks, the computed damping factor should be non-negative and less than 1 (0 <= zeta < 1 for underdamped systems).
**Validates: Requirements 4.1, 4.2, 4.3**

**Property 9: Natural frequency detection excludes DC**
_For any_ FFT spectrum, the detected natural frequency should be greater than zero (excluding DC component).
**Validates: Requirements 5.1, 5.5**

**Property 10: Exponential decay lifetime model**
_For any_ signal with computed damping factor and natural frequency, the time-domain lifetime should be inversely proportional to the product (zeta \* omega_n).
**Validates: Requirements 6.1, 6.2, 6.5**

**Property 11: Spectral energy calculation**
_For any_ FFT amplitude spectrum, the spectral energy should equal the sum of squared amplitudes: E = sum(A(f)²).
**Validates: Requirements 7.1**

**Property 12: Energy-lifetime inverse relationship**
_For any_ two signals with different spectral energies E1 and E2 where E1 > E2, the frequency-domain lifetime for signal 1 should be less than signal 2 (higher energy → shorter lifetime).
**Validates: Requirements 7.2**

**Property 13: Frequency shift lifetime calculation**
_For any_ detected natural frequency, the natural frequency shift lifetime should be inversely proportional to the absolute difference from baseline: lifetime ∝ 1/|f_n - f_baseline|.
**Validates: Requirements 8.1, 8.2**

**Property 14: Damping-lifetime inverse relationship**
_For any_ two signals with different damping factors zeta1 and zeta2 where zeta1 > zeta2, the damping-based lifetime for signal 1 should be less than signal 2 (higher damping → shorter lifetime).
**Validates: Requirements 9.1**

**Property 15: Lifetime bounds**
_For any_ computed lifetime estimate (time, frequency, natural, or damping based), the value should be within a reasonable range (e.g., 10 to 10000 hours).
**Validates: Requirements 7.4, 9.4**

**Property 16: Weighted average formula**
_For any_ four lifetime components (L_time, L_freq, L_natural, L_damping), the weighted average should equal: L_avg = 0.25 _ L_time + 0.25 _ L_freq + 0.25 _ L_natural + 0.25 _ L_damping.
**Validates: Requirements 10.1**

**Property 17: Average lifetime preconditions**
_For any_ computation of average lifetime, all four component lifetimes should be available (non-zero or non-null) before the average is computed.
**Validates: Requirements 10.3**

**Property 18: Average lifetime reactivity**
_For any_ change to a component lifetime value, the weighted average lifetime should be recalculated and updated.
**Validates: Requirements 10.5**

### Backend AI Model Properties

**Property 19: AI feature extraction**
_For any_ processed vibration data, the AI model should receive exactly 5 features: RMS acceleration, peak acceleration, damping factor, natural frequency, and spectral energy.
**Validates: Requirements 11.2**

**Property 20: AI prediction non-negativity**
_For any_ AI lifetime prediction, the predicted value should be non-negative (ai_lifetime >= 0).
**Validates: Requirements 11.3, 11.4**

### Backend API Properties

**Property 21: Conditional data response**
_For any_ GET request to /get-data, when new_data_available is true, the response should include new data arrays; when false, it should return cached results.
**Validates: Requirements 12.1, 12.2**

**Property 22: Full refresh completeness**
_For any_ GET request to /full-refresh, the response should include all fields: time, acceleration, frequency, amplitude, damping_factor, natural_frequency, all four lifetime estimates, average_lifetime, and ai_lifetime.
**Validates: Requirements 12.3**

**Property 23: Flag reset on retrieval**
_For any_ successful GET request to /get-data, the new_data_available flag should be set to false after the response is sent.
**Validates: Requirements 12.4**

**Property 24: JSON response format**
_For any_ API response, the data should be valid JSON containing all required metric fields.
**Validates: Requirements 12.5**

### Simulator Properties

**Property 25: Damped oscillation formula**
_For any_ generated vibration signal, the acceleration values should follow the pattern: x(t) = A _ exp(-zeta _ omega _ t) _ sin(omega \* t) plus noise.
**Validates: Requirements 13.1**

**Property 26: Simulator output format**
_For any_ generated signal, the simulator should produce JSON with "time" and "acceleration" arrays of equal length.
**Validates: Requirements 13.4**

**Property 27: Simulator parameter influence**
_For any_ two simulations with different amplitude parameters A1 and A2 where A1 > A2, the maximum absolute acceleration in simulation 1 should be greater than simulation 2.
**Validates: Requirements 13.5**

### Frontend Update Properties

**Property 28: Incremental chart updates**
_For any_ response where new_data_available is true, the Frontend should update both time-domain and frequency-domain charts with the new data.
**Validates: Requirements 14.2, 14.4, 14.5**

**Property 29: Natural frequency peak highlighting**
_For any_ frequency spectrum display, the Frontend should visually highlight the frequency corresponding to the detected natural frequency.
**Validates: Requirements 16.3**

**Property 30: Damping factor display update**
_For any_ new damping factor value received from the backend, the Frontend should update the numeric display and gauge visualization.
**Validates: Requirements 17.3**

**Property 31: Damping factor precision**
_For any_ damping factor display, the numeric value should be formatted with 3-4 decimal places.
**Validates: Requirements 17.4**

**Property 32: Damping color coding**
_For any_ damping factor value, the Frontend should apply color coding based on whether the value is in normal or abnormal range.
**Validates: Requirements 17.5**

**Property 33: Natural frequency display update**
_For any_ new natural frequency value received from the backend, the Frontend should update the numeric display.
**Validates: Requirements 18.3**

**Property 34: Frequency shift indication**
_For any_ natural frequency that differs from baseline by more than a threshold, the Frontend should display a visual indicator.
**Validates: Requirements 18.4**

**Property 35: Frequency display precision**
_For any_ natural frequency display, the numeric value should be formatted with appropriate precision (e.g., 2 decimal places).
**Validates: Requirements 18.5**

**Property 36: Percentage difference calculation**
_For any_ AI prediction and average lifetime values, the Frontend should compute and display the percentage difference as: |ai_lifetime - average_lifetime| / average_lifetime \* 100.
**Validates: Requirements 20.3**

**Property 37: Comparison color coding**
_For any_ percentage difference between AI prediction and average lifetime, the Frontend should apply color coding (e.g., green for < 10% difference, red for > 20% difference).
**Validates: Requirements 20.4**

**Property 38: Comparison panel updates**
_For any_ new AI prediction or average lifetime value, the Frontend should update the comparison panel with the new values and recalculated percentage difference.
**Validates: Requirements 20.5**

### Error Handling Properties

**Property 39: Invalid JSON error response**
_For any_ malformed JSON sent to /send-data, the Backend should return an HTTP error response (4xx status code) with an error message.
**Validates: Requirements 25.1**

## Error Handling

### Backend Error Handling

**Data Validation:**

- Validate JSON structure and data types on /send-data endpoint
- Return 400 Bad Request for invalid formats
- Validate array lengths match (time and acceleration)
- Validate numeric values are finite (not NaN or Inf)

**Computation Errors:**

- Wrap FFT computation in try-catch blocks
- If FFT fails, log error and return previous valid results
- If damping calculation fails (insufficient peaks), use default value (0.05)
- If natural frequency detection fails, return 0.0

**AI Model Errors:**

- Wrap AI prediction in try-catch blocks
- If AI model fails, fall back to average lifetime estimate
- Log AI errors for debugging

**File I/O Errors:**

- If data_store.json is missing, create with default structure
- If data_store.json is corrupted, backup and reinitialize
- Use file locking for concurrent access protection
- Implement retry logic for transient file system errors

**Graceful Degradation:**

- System should continue operating even if individual components fail
- Return partial results when possible
- Maintain last known good state

### Frontend Error Handling

**Network Errors:**

- Catch fetch() errors and display user-friendly messages
- Implement retry logic with exponential backoff
- Show connection status indicator

**Data Validation:**

- Validate API responses before updating UI
- Handle missing or null values gracefully
- Prevent chart rendering errors with empty data

**User Feedback:**

- Display error messages in a dedicated error panel
- Use toast notifications for transient errors
- Provide clear error descriptions and suggested actions

## Testing Strategy

### Dual Testing Approach

This system requires both unit testing and property-based testing for comprehensive coverage:

**Unit Tests:**

- Verify specific examples and edge cases
- Test integration points between components
- Validate error conditions and boundary cases
- Test specific UI interactions and rendering

**Property-Based Tests:**

- Verify universal properties across all inputs
- Test mathematical relationships and invariants
- Validate behavior across wide input ranges
- Ensure correctness properties hold for random inputs

Both testing approaches are complementary and necessary. Unit tests catch concrete bugs in specific scenarios, while property-based tests verify general correctness across the input space.

### Property-Based Testing Configuration

**Framework Selection:**

- Python backend: Use `hypothesis` library for property-based testing
- JavaScript frontend: Use `fast-check` library for property-based testing

**Test Configuration:**

- Minimum 100 iterations per property test (due to randomization)
- Each property test must reference its design document property
- Tag format: `# Feature: vibration-lifetime-prediction, Property {number}: {property_text}`

**Example Property Test Structure (Python):**

```python
from hypothesis import given, strategies as st
import numpy as np

@given(
    time=st.lists(st.floats(min_value=0, max_value=10), min_size=10, max_size=1000),
    acceleration=st.lists(st.floats(min_value=-100, max_value=100), min_size=10, max_size=1000)
)
def test_property_2_data_append_behavior(time, acceleration):
    """
    Feature: vibration-lifetime-prediction, Property 2: Data append behavior
    For any existing data store and new data chunk, when new data is received,
    the Backend should append the new data such that the total length equals
    the sum of previous length and new data length.
    """
    # Arrange
    initial_length = len(load_data_store()['time'])

    # Act
    append_data(time, acceleration)

    # Assert
    final_length = len(load_data_store()['time'])
    assert final_length == initial_length + len(time)
```

### Unit Testing Strategy

**Backend Unit Tests:**

- Test each signal processing function with known inputs
- Test API endpoints with mock data
- Test error handling with invalid inputs
- Test file I/O operations with temporary files
- Test AI model with synthetic training data

**Frontend Unit Tests:**

- Test data fetching functions with mocked fetch()
- Test chart update functions with sample data
- Test metric calculation functions
- Test error display functions
- Test UI state management

**Integration Tests:**

- Test complete data flow from /send-data to /get-data
- Test simulator → backend → frontend pipeline
- Test concurrent data submissions
- Test server restart and data persistence

### Test Coverage Goals

- Backend code coverage: > 80%
- Frontend code coverage: > 70%
- All correctness properties: 100% (each property must have a test)
- All error handling paths: 100%

### Testing Edge Cases

The property-based test generators should be configured to include edge cases:

**Signal Processing Edge Cases:**

- Empty arrays
- Single-element arrays
- Constant signals (no oscillation)
- Pure noise (no clear frequency)
- Signals with multiple peaks
- Very high or very low frequencies
- Zero or negative damping

**API Edge Cases:**

- Empty JSON payloads
- Mismatched array lengths
- Non-numeric values
- Very large datasets
- Concurrent requests

**Frontend Edge Cases:**

- Backend unavailable
- Malformed API responses
- Missing data fields
- Zero or null values
- Very large or very small numbers

### Continuous Testing

- Run unit tests on every code change
- Run property-based tests in CI/CD pipeline
- Monitor test execution time (property tests may be slower)
- Generate test coverage reports
- Track property test failure rates and counterexamples
