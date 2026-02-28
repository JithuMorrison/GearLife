# Requirements Document

## Introduction

This document specifies the requirements for a Mechanical System Lifetime Prediction Platform - a full-stack real-time vibration analysis and AI-based predictive maintenance system. The system receives real-time acceleration time-series data, performs signal processing (FFT, damping factor, natural frequency detection), computes multiple lifetime estimates using both traditional methods and AI, and displays all metrics in a professional industrial UI with real-time updates.

## Glossary

- **System**: The Mechanical System Lifetime Prediction Platform
- **Backend**: The Python FastAPI server that processes vibration data
- **Frontend**: The web-based user interface displaying real-time metrics
- **FFT**: Fast Fourier Transform - converts time-domain signals to frequency-domain
- **Damping_Factor**: A dimensionless measure of oscillation decay (zeta)
- **Natural_Frequency**: The frequency at which a system naturally oscillates
- **IEPE**: Integrated Electronics Piezo-Electric sensor format
- **Data_Store**: JSON file containing all vibration data and computed metrics
- **Simulator**: Component that generates synthetic vibration data for testing
- **AI_Model**: Machine learning regression model for lifetime prediction
- **Lifetime_Estimate**: Predicted remaining operational time of the mechanical system

## Requirements

### Requirement 1: Real-Time Data Ingestion

**User Story:** As a maintenance engineer, I want to send real-time vibration data to the system, so that I can monitor equipment health continuously.

#### Acceptance Criteria

1. WHEN vibration data is sent via POST request to /send-data endpoint, THE Backend SHALL accept JSON containing time and acceleration arrays
2. WHEN new data is received, THE Backend SHALL append only new data points to the Data_Store
3. WHEN new data is appended, THE Backend SHALL set a new_data_available flag to true
4. THE Backend SHALL accept data in the format: {"time": [], "acceleration": []}
5. WHEN data is received, THE Backend SHALL trigger recalculation of all signal processing and lifetime metrics

### Requirement 2: Data Persistence

**User Story:** As a system administrator, I want all vibration data and computed metrics stored persistently, so that I can review historical analysis results.

#### Acceptance Criteria

1. THE Backend SHALL store all data in a JSON file named data_store.json
2. THE Data_Store SHALL contain fields for: time, acceleration, frequency, amplitude, damping_factor, natural_frequency, lifetime_time, lifetime_freq, lifetime_natural, lifetime_damping, average_lifetime, ai_lifetime, and new_data_available
3. WHEN new data arrives, THE Backend SHALL append to existing arrays without overwriting previous data
4. THE Data_Store SHALL persist between server restarts
5. THE Backend SHALL maintain data integrity during concurrent read/write operations

### Requirement 3: Fast Fourier Transform Processing

**User Story:** As a vibration analyst, I want the system to convert time-domain signals to frequency-domain, so that I can identify frequency components in the vibration signature.

#### Acceptance Criteria

1. WHEN new acceleration data is received, THE Backend SHALL perform FFT conversion on the time-domain signal
2. THE Backend SHALL compute a frequency array from the FFT results
3. THE Backend SHALL compute an amplitude spectrum from the FFT results
4. THE Backend SHALL store the frequency and amplitude arrays in the Data_Store
5. THE FFT SHALL use the numpy or scipy FFT implementation for accuracy

### Requirement 4: Damping Factor Calculation

**User Story:** As a mechanical engineer, I want the system to calculate the damping factor, so that I can assess energy dissipation in the system.

#### Acceptance Criteria

1. WHEN amplitude data is available, THE Backend SHALL calculate damping factor using logarithmic decrement method
2. THE Backend SHALL compute delta as ln(x1/x2) where x1 and x2 are successive peak amplitudes
3. THE Backend SHALL compute zeta (damping factor) as delta / sqrt(4π² + delta²)
4. THE Backend SHALL store the computed damping_factor in the Data_Store
5. IF insufficient peaks are detected, THE Backend SHALL return a default damping factor value

### Requirement 5: Natural Frequency Detection

**User Story:** As a vibration analyst, I want the system to detect the natural frequency, so that I can identify resonance conditions.

#### Acceptance Criteria

1. WHEN FFT amplitude spectrum is computed, THE Backend SHALL identify the peak frequency
2. THE Backend SHALL set natural_frequency as the frequency corresponding to maximum amplitude
3. THE Backend SHALL store the natural_frequency in the Data_Store
4. THE Backend SHALL handle cases where multiple peaks exist by selecting the dominant peak
5. THE Backend SHALL exclude DC component (zero frequency) from peak detection

### Requirement 6: Time-Domain Lifetime Calculation

**User Story:** As a maintenance planner, I want lifetime estimated from amplitude decay, so that I can schedule maintenance based on signal envelope degradation.

#### Acceptance Criteria

1. WHEN time and amplitude data are available, THE Backend SHALL fit an exponential decay model: A(t) = A0 _ exp(-zeta _ omega_n \* t)
2. THE Backend SHALL estimate time until amplitude falls below a predefined threshold
3. THE Backend SHALL store the computed lifetime_time in the Data_Store
4. THE Backend SHALL handle cases where decay is not detectable by returning a maximum lifetime value
5. THE Backend SHALL use the computed damping factor and natural frequency in the decay model

### Requirement 7: Frequency-Domain Lifetime Calculation

**User Story:** As a condition monitoring specialist, I want lifetime estimated from spectral energy, so that I can assess overall vibration energy levels.

#### Acceptance Criteria

1. WHEN FFT amplitude spectrum is available, THE Backend SHALL compute spectral energy as sum(A(f)²)
2. THE Backend SHALL calculate lifetime inversely proportional to spectral energy
3. THE Backend SHALL store the computed lifetime_freq in the Data_Store
4. THE Backend SHALL normalize energy values to produce meaningful lifetime estimates
5. THE Backend SHALL handle zero or near-zero energy cases gracefully

### Requirement 8: Natural Frequency Shift Lifetime Calculation

**User Story:** As a structural health monitoring engineer, I want lifetime estimated from natural frequency shifts, so that I can detect structural degradation.

#### Acceptance Criteria

1. WHEN natural frequency is detected, THE Backend SHALL compare it with a baseline natural frequency
2. THE Backend SHALL calculate lifetime proportional to 1 / |f_n - f_baseline|
3. THE Backend SHALL store the computed lifetime_natural in the Data_Store
4. THE Backend SHALL define a baseline natural frequency value
5. THE Backend SHALL handle cases where detected frequency equals baseline by returning maximum lifetime

### Requirement 9: Damping-Based Lifetime Calculation

**User Story:** As a reliability engineer, I want lifetime estimated from damping factor, so that I can assess wear-related degradation.

#### Acceptance Criteria

1. WHEN damping factor is computed, THE Backend SHALL calculate lifetime inversely proportional to damping factor
2. THE Backend SHALL apply the principle that higher damping implies increased wear and reduced lifetime
3. THE Backend SHALL store the computed lifetime_damping in the Data_Store
4. THE Backend SHALL normalize damping values to produce meaningful lifetime estimates
5. THE Backend SHALL handle zero or negative damping values gracefully

### Requirement 10: Weighted Average Lifetime Calculation

**User Story:** As a maintenance manager, I want a single aggregated lifetime estimate, so that I can make unified maintenance decisions.

#### Acceptance Criteria

1. WHEN all four lifetime estimates are computed, THE Backend SHALL calculate weighted average: L_avg = 0.25 _ L_time + 0.25 _ L_freq + 0.25 _ L_natural + 0.25 _ L_damping
2. THE Backend SHALL store the computed average_lifetime in the Data_Store
3. THE Backend SHALL ensure all four lifetime components are available before computing average
4. THE Backend SHALL use equal weights (0.25) for each lifetime component
5. THE Backend SHALL update the average whenever any component lifetime changes

### Requirement 11: AI-Based Lifetime Prediction

**User Story:** As a data scientist, I want an AI model to predict lifetime from multiple features, so that I can leverage machine learning for more accurate predictions.

#### Acceptance Criteria

1. THE Backend SHALL implement a regression model (MLP or RandomForest) for lifetime prediction
2. THE AI_Model SHALL accept input features: RMS acceleration, peak acceleration, damping factor, natural frequency, and spectral energy
3. WHEN all input features are computed, THE Backend SHALL invoke the AI_Model to predict lifetime
4. THE Backend SHALL store the ai_lifetime prediction in the Data_Store
5. THE AI_Model SHALL be trained on representative vibration data before deployment

### Requirement 12: Data Retrieval Endpoints

**User Story:** As a frontend developer, I want efficient data retrieval endpoints, so that I can update the UI without unnecessary data transfer.

#### Acceptance Criteria

1. THE Backend SHALL provide a GET /get-data endpoint that returns only new processed results when new_data_available is true
2. WHEN new_data_available is false, THE Backend SHALL return the last computed state from /get-data
3. THE Backend SHALL provide a GET /full-refresh endpoint that returns the complete dataset and all processed results
4. WHEN data is retrieved via /get-data, THE Backend SHALL set new_data_available to false
5. THE Backend SHALL return data in JSON format with all computed metrics

### Requirement 13: Vibration Data Simulation

**User Story:** As a system tester, I want simulated vibration data, so that I can test the system without physical sensors.

#### Acceptance Criteria

1. THE Simulator SHALL generate vibration signals using the formula: x(t) = A _ exp(-zeta _ omega _ t) _ sin(omega \* t)
2. THE Simulator SHALL send periodic data chunks to the /send-data endpoint
3. THE Simulator SHALL simulate realistic damping and frequency parameters
4. THE Simulator SHALL generate time and acceleration arrays in the required JSON format
5. THE Simulator SHALL allow configuration of simulation parameters (amplitude, frequency, damping)

### Requirement 14: Real-Time Frontend Updates

**User Story:** As an operator, I want the dashboard to update automatically, so that I can monitor equipment health without manual refresh.

#### Acceptance Criteria

1. THE Frontend SHALL poll the /get-data endpoint every 2 seconds
2. WHEN new_data_available is true, THE Frontend SHALL update all graphs and metrics incrementally
3. WHEN the page is refreshed, THE Frontend SHALL call /full-refresh to load complete data
4. THE Frontend SHALL update time vs amplitude graph in real-time
5. THE Frontend SHALL update frequency vs amplitude graph in real-time

### Requirement 15: Time-Domain Visualization

**User Story:** As a vibration analyst, I want to see time-domain acceleration data, so that I can identify transient events and trends.

#### Acceptance Criteria

1. THE Frontend SHALL display a time vs amplitude line chart
2. THE Frontend SHALL update the chart incrementally when new data arrives
3. THE Frontend SHALL use appropriate axis labels and units
4. THE Frontend SHALL handle large datasets efficiently without performance degradation
5. THE Frontend SHALL provide clear visual representation of amplitude variations over time

### Requirement 16: Frequency-Domain Visualization

**User Story:** As a frequency analyst, I want to see the FFT spectrum, so that I can identify dominant frequency components.

#### Acceptance Criteria

1. THE Frontend SHALL display a frequency vs amplitude line chart showing the FFT spectrum
2. THE Frontend SHALL update the spectrum chart when new FFT data is computed
3. THE Frontend SHALL highlight the natural frequency peak on the spectrum
4. THE Frontend SHALL use logarithmic or linear scale as appropriate for amplitude display
5. THE Frontend SHALL provide clear axis labels indicating frequency units (Hz)

### Requirement 17: Damping Factor Display

**User Story:** As a mechanical engineer, I want to see the current damping factor, so that I can assess energy dissipation characteristics.

#### Acceptance Criteria

1. THE Frontend SHALL display the damping factor as a numeric value
2. THE Frontend SHALL display the damping factor using a circular gauge visualization
3. THE Frontend SHALL update the damping factor display when new values are computed
4. THE Frontend SHALL use appropriate precision (e.g., 3-4 decimal places) for the numeric display
5. THE Frontend SHALL indicate normal vs abnormal damping ranges using color coding

### Requirement 18: Natural Frequency Display

**User Story:** As a resonance analyst, I want to see the detected natural frequency, so that I can monitor for resonance conditions.

#### Acceptance Criteria

1. THE Frontend SHALL display the natural frequency as a numeric value with units (Hz)
2. THE Frontend SHALL highlight the natural frequency peak on the FFT spectrum chart
3. THE Frontend SHALL update the natural frequency display when new values are detected
4. THE Frontend SHALL provide visual indication when natural frequency shifts from baseline
5. THE Frontend SHALL use appropriate precision for frequency display

### Requirement 19: Lifetime Calculations Display Panel

**User Story:** As a maintenance planner, I want to see all lifetime estimates, so that I can compare different calculation methods.

#### Acceptance Criteria

1. THE Frontend SHALL display lifetime_time (time-domain based) with appropriate units
2. THE Frontend SHALL display lifetime_freq (frequency-domain based) with appropriate units
3. THE Frontend SHALL display lifetime_natural (natural frequency shift based) with appropriate units
4. THE Frontend SHALL display lifetime_damping (damping-based) with appropriate units
5. THE Frontend SHALL display the weighted average_lifetime prominently

### Requirement 20: AI Prediction Comparison Panel

**User Story:** As a data analyst, I want to compare AI predictions with traditional methods, so that I can evaluate model performance.

#### Acceptance Criteria

1. THE Frontend SHALL display the ai_lifetime prediction with appropriate units
2. THE Frontend SHALL display the average_lifetime alongside the AI prediction
3. THE Frontend SHALL compute and display the percentage difference between AI prediction and average lifetime
4. THE Frontend SHALL use visual indicators (color coding) to show agreement or divergence
5. THE Frontend SHALL update the comparison panel when new predictions are available

### Requirement 21: Professional Industrial UI Theme

**User Story:** As an end user, I want a professional mechanical-themed interface, so that the system feels appropriate for industrial monitoring.

#### Acceptance Criteria

1. THE Frontend SHALL use a dark industrial background color scheme
2. THE Frontend SHALL incorporate steel or gunmetal textures in the design
3. THE Frontend SHALL use neon blue or cyan accent lines for highlights
4. THE Frontend SHALL include subtle grid overlays for a technical appearance
5. THE Frontend SHALL use industrial typography (monospace or technical fonts)

### Requirement 22: Visual Enhancements

**User Story:** As an operator, I want engaging visual elements, so that the interface is both functional and visually appealing.

#### Acceptance Criteria

1. THE Frontend SHALL include animated gear SVG graphics as decorative elements
2. THE Frontend SHALL use a data-intensive dashboard layout with multiple panels
3. THE Frontend SHALL provide smooth transitions when updating metrics
4. THE Frontend SHALL maintain visual consistency across all components
5. THE Frontend SHALL ensure all text is readable against the dark background

### Requirement 23: Backend Environment Setup

**User Story:** As a developer, I want a properly configured backend environment, so that all dependencies are managed correctly.

#### Acceptance Criteria

1. THE Backend SHALL run inside a Python virtual environment located at backend/venv
2. THE Backend SHALL use FastAPI as the web framework
3. THE Backend SHALL include dependencies: fastapi, uvicorn, numpy, scipy, scikit-learn, and asyncio support
4. THE Backend SHALL provide a requirements.txt file listing all dependencies
5. THE Backend SHALL support Python 3.8 or higher

### Requirement 24: Project Structure Organization

**User Story:** As a developer, I want a clear project structure, so that code is organized and maintainable.

#### Acceptance Criteria

1. THE System SHALL organize backend code in a backend/ directory containing: app.py, ai_model.py, signal_processing.py, simulator.py, data_store.json, and requirements.txt
2. THE System SHALL organize frontend code in a frontend/ directory containing: index.html, style.css, and script.js
3. THE Backend SHALL separate concerns: API endpoints in app.py, signal processing in signal_processing.py, AI model in ai_model.py
4. THE System SHALL maintain the virtual environment in backend/venv
5. THE System SHALL provide clear separation between backend and frontend codebases

### Requirement 25: Error Handling and Edge Cases

**User Story:** As a system operator, I want the system to handle errors gracefully, so that unexpected inputs don't crash the application.

#### Acceptance Criteria

1. WHEN invalid JSON is sent to /send-data, THE Backend SHALL return an appropriate error response
2. WHEN FFT computation fails, THE Backend SHALL log the error and return previous valid results
3. WHEN AI model prediction fails, THE Backend SHALL fall back to average lifetime estimate
4. WHEN data_store.json is corrupted, THE Backend SHALL initialize with default values
5. THE Frontend SHALL display error messages when backend communication fails
