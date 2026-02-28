# GearLife - Vibration Lifetime Prediction Platform

A full-stack real-time vibration analysis and AI-based predictive maintenance system for mechanical systems.

## Project Structure

```
GearLife/
├── backend/                    # Python FastAPI backend
│   ├── venv/                  # Python virtual environment
│   ├── app.py                 # FastAPI application
│   ├── signal_processing.py   # Signal processing functions
│   ├── ai_model.py            # AI model for lifetime prediction
│   ├── simulator.py           # Vibration data simulator
│   ├── data_store.json        # Persistent data storage
│   └── requirements.txt       # Python dependencies
│
├── src/                       # React frontend
│   ├── components/            # React components
│   │   ├── Header.tsx         # Header with connection status
│   │   ├── TimeChart.tsx      # Time-domain visualization
│   │   ├── FrequencyChart.tsx # Frequency-domain visualization
│   │   ├── DampingPanel.tsx   # Damping factor display
│   │   ├── FrequencyPanel.tsx # Natural frequency display
│   │   ├── LifetimePanel.tsx  # Lifetime estimates
│   │   ├── AIComparisonPanel.tsx # AI vs traditional comparison
│   │   └── ErrorPanel.tsx     # Error message display
│   ├── App.tsx                # Main application component
│   └── main.tsx               # Application entry point
│
└── package.json               # Node.js dependencies
```

## Setup Instructions

### Backend Setup

1. **Navigate to backend directory:**

   ```bash
   cd backend
   ```

2. **Activate virtual environment:**
   - Windows:
     ```bash
     venv\Scripts\activate
     ```
   - Linux/Mac:
     ```bash
     source venv/bin/activate
     ```

3. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Run the backend server:**

   ```bash
   python app.py
   ```

   The backend will start on `http://localhost:8000`

### Frontend Setup

1. **Install Node.js dependencies:**

   ```bash
   npm install
   ```

2. **Run the development server:**

   ```bash
   npm run dev
   ```

   The frontend will start on `http://localhost:5173`

### Running the Simulator (Optional)

To test the system with simulated vibration data:

```bash
cd backend
python simulator.py
```

## Features

- **Real-time Data Ingestion**: Accepts vibration data via REST API
- **Signal Processing**: FFT, damping factor calculation, natural frequency detection
- **Multiple Lifetime Estimates**: Time-domain, frequency-domain, natural frequency shift, and damping-based
- **AI Prediction**: Machine learning model for enhanced lifetime prediction
- **Industrial UI**: Professional dark-themed dashboard with real-time updates
- **Data Persistence**: All data and metrics stored in JSON format

## API Endpoints

- `POST /send-data` - Submit vibration data
- `GET /get-data` - Retrieve processed results (incremental)
- `GET /full-refresh` - Retrieve complete dataset

## Technology Stack

**Backend:**

- FastAPI (Python web framework)
- NumPy (numerical computing)
- SciPy (signal processing)
- scikit-learn (machine learning)
- Hypothesis (property-based testing)

**Frontend:**

- React 19 with TypeScript
- Vite (build tool)
- CSS3 (industrial styling)

## Development

- Backend runs on port 8000
- Frontend runs on port 5173 (Vite default)
- CORS is configured for local development

## Testing

Property-based tests are included for core functionality. Run tests with:

```bash
cd backend
pytest
```

## License

MIT
