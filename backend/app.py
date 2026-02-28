# FastAPI application for vibration lifetime prediction
# This module handles API endpoints and orchestrates signal processing

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import json
import os
import numpy as np
from typing import List, Dict, Any

app = FastAPI(title="Vibration Lifetime Prediction API")

# Configure CORS for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Data models
class SendDataRequest(BaseModel):
    time: List[float]
    acceleration: List[float]

# Data store file path
DATA_STORE_PATH = os.path.join(os.path.dirname(__file__), "data_store.json")

# Data store management functions

def init_data_store() -> Dict[str, Any]:
    """
    Initialize data store with default JSON structure
    
    Returns:
        dict: Default data store structure with all required fields
    
    Requirements: 2.1, 2.2
    """
    return {
        "time": [],
        "acceleration": [],
        "frequency": [],
        "amplitude": [],
        "damping_factor": 0.0,
        "natural_frequency": 0.0,
        "lifetime_time": 0.0,
        "lifetime_freq": 0.0,
        "lifetime_natural": 0.0,
        "lifetime_damping": 0.0,
        "average_lifetime": 0.0,
        "ai_lifetime": 0.0,
        "new_data_available": False
    }

def load_data_store() -> Dict[str, Any]:
    """
    Load data store from data_store.json file
    
    Handles file not found and corrupted file errors by initializing
    with default structure.
    
    Returns:
        dict: Data store contents
    
    Requirements: 2.4, 25.4
    """
    try:
        # Check if file exists
        if not os.path.exists(DATA_STORE_PATH):
            # Initialize with default structure
            default_data = init_data_store()
            save_data_store(default_data)
            return default_data
        
        # Read file
        with open(DATA_STORE_PATH, 'r') as f:
            data = json.load(f)
            # Validate that all required fields exist
            default_data = init_data_store()
            for key in default_data.keys():
                if key not in data:
                    raise ValueError(f"Missing required field: {key}")
            return data
    except (json.JSONDecodeError, ValueError) as e:
        # Corrupted file - backup and reinitialize
        print(f"Error loading data store: {e}. Reinitializing with defaults.")
        backup_path = DATA_STORE_PATH + ".backup"
        if os.path.exists(DATA_STORE_PATH):
            try:
                os.rename(DATA_STORE_PATH, backup_path)
            except:
                pass  # Backup failed, continue anyway
        default_data = init_data_store()
        save_data_store(default_data)
        return default_data
    except Exception as e:
        print(f"Unexpected error loading data store: {e}. Using default structure.")
        return init_data_store()

def save_data_store(data: Dict[str, Any]) -> None:
    """
    Save data store to data_store.json file
    
    Args:
        data: Data store dictionary to save
    
    Requirements: 2.4, 25.4
    """
    try:
        with open(DATA_STORE_PATH, 'w') as f:
            json.dump(data, f, indent=2)
    except Exception as e:
        print(f"Error saving data store: {e}")
        raise

def append_data(new_time: List[float], new_acceleration: List[float]) -> None:
    """
    Append new time/acceleration data to the data store
    
    Appends to existing arrays without overwriting previous data.
    Sets new_data_available flag to true.
    
    Args:
        new_time: New time values to append
        new_acceleration: New acceleration values to append
    
    Requirements: 1.2, 1.3, 2.3
    """
    # Load current data store
    data = load_data_store()
    
    # Append new data to existing arrays
    data["time"].extend(new_time)
    data["acceleration"].extend(new_acceleration)
    
    # Set new_data_available flag to true
    data["new_data_available"] = True
    
    # Save updated data store
    save_data_store(data)

def trigger_processing() -> None:
    """
    Orchestrate signal processing and AI prediction pipeline
    
    This function:
    1. Loads current data from data store
    2. Performs FFT computation
    3. Calculates damping factor and natural frequency
    4. Computes all four lifetime estimates
    5. Calculates weighted average lifetime
    6. Performs AI prediction
    7. Saves all results back to data store
    
    Requirements: 1.5, 3.4, 4.4, 5.3, 6.3, 7.3, 8.3, 9.3, 10.2, 11.4
    """
    import numpy as np
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
    from ai_model import predict_lifetime
    import pickle
    
    # Load current data store
    data = load_data_store()
    
    # Convert lists to numpy arrays for processing
    time = np.array(data["time"])
    acceleration = np.array(data["acceleration"])
    
    # Skip processing if no data available
    if len(time) == 0 or len(acceleration) == 0:
        return
    
    # Step 1: Compute FFT
    frequency, amplitude = compute_fft(time, acceleration)
    data["frequency"] = frequency.tolist()
    data["amplitude"] = amplitude.tolist()
    
    # Step 2: Calculate damping factor
    damping_factor = calculate_damping_factor(time, acceleration)
    data["damping_factor"] = float(damping_factor)
    
    # Step 3: Detect natural frequency
    natural_frequency = detect_natural_frequency(frequency, amplitude)
    data["natural_frequency"] = float(natural_frequency)
    
    # Step 4: Calculate all four lifetime estimates
    omega_n = 2 * np.pi * natural_frequency if natural_frequency > 0 else 0
    
    lifetime_time = calculate_lifetime_time_domain(
        time, acceleration, damping_factor, omega_n
    )
    data["lifetime_time"] = float(lifetime_time)
    
    lifetime_freq = calculate_lifetime_frequency_domain(frequency, amplitude)
    data["lifetime_freq"] = float(lifetime_freq)
    
    lifetime_natural = calculate_lifetime_natural_frequency(natural_frequency)
    data["lifetime_natural"] = float(lifetime_natural)
    
    lifetime_damping = calculate_lifetime_damping(damping_factor)
    data["lifetime_damping"] = float(lifetime_damping)
    
    # Step 5: Calculate weighted average lifetime
    average_lifetime = calculate_weighted_average_lifetime(
        lifetime_time, lifetime_freq, lifetime_natural, lifetime_damping
    )
    data["average_lifetime"] = float(average_lifetime)
    
    # Step 6: AI prediction
    try:
        # Try to load trained model
        model_path = os.path.join(os.path.dirname(__file__), "trained_model.pkl")
        if os.path.exists(model_path):
            with open(model_path, 'rb') as f:
                model = pickle.load(f)
            
            ai_lifetime = predict_lifetime(
                model, acceleration, damping_factor, natural_frequency, 
                amplitude, average_lifetime
            )
            data["ai_lifetime"] = float(ai_lifetime)
        else:
            # No trained model available, use average lifetime as fallback
            data["ai_lifetime"] = float(average_lifetime) if average_lifetime > 0 else 1000.0
    except Exception as e:
        print(f"AI prediction failed: {e}. Using average lifetime as fallback.")
        data["ai_lifetime"] = float(average_lifetime) if average_lifetime > 0 else 1000.0
    
    # Step 7: Save all results to data store
    save_data_store(data)

# API Endpoints

@app.post("/send-data")
async def send_data(request: SendDataRequest):
    """
    Accept vibration data and trigger processing
    
    This endpoint:
    1. Validates input format and data types
    2. Appends new data to data store
    3. Triggers signal processing pipeline
    4. Returns success response
    
    Requirements: 1.1, 1.4, 25.1
    """
    try:
        # Validate input format
        if not isinstance(request.time, list) or not isinstance(request.acceleration, list):
            raise HTTPException(
                status_code=400,
                detail="Invalid data format. Expected 'time' and 'acceleration' as arrays."
            )
        
        # Validate array lengths match
        if len(request.time) != len(request.acceleration):
            raise HTTPException(
                status_code=400,
                detail="Time and acceleration arrays must have the same length."
            )
        
        # Validate arrays are not empty
        if len(request.time) == 0:
            raise HTTPException(
                status_code=400,
                detail="Time and acceleration arrays cannot be empty."
            )
        
        # Validate all values are finite numbers
        for val in request.time:
            if not isinstance(val, (int, float)) or not np.isfinite(val):
                raise HTTPException(
                    status_code=400,
                    detail="All time values must be finite numbers."
                )
        
        for val in request.acceleration:
            if not isinstance(val, (int, float)) or not np.isfinite(val):
                raise HTTPException(
                    status_code=400,
                    detail="All acceleration values must be finite numbers."
                )
        
        # Append data to data store
        append_data(request.time, request.acceleration)
        
        # Trigger signal processing pipeline
        trigger_processing()
        
        return {
            "status": "success",
            "message": "Data received and processed"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Error processing data: {str(e)}"
        )

@app.get("/get-data")
async def get_data():
    """
    Return processed data if new data is available
    
    This endpoint:
    1. Checks new_data_available flag
    2. Returns new data and metrics if flag is true
    3. Returns cached results if flag is false
    4. Sets new_data_available to false after retrieval
    
    Requirements: 12.1, 12.2, 12.4, 12.5
    """
    try:
        # Load current data store
        data = load_data_store()
        
        # Check if new data is available
        new_data_available = data.get("new_data_available", False)
        
        # Prepare response
        response = {
            "new_data_available": new_data_available,
            "frequency": data.get("frequency", []),
            "amplitude": data.get("amplitude", []),
            "damping_factor": data.get("damping_factor", 0.0),
            "natural_frequency": data.get("natural_frequency", 0.0),
            "lifetime_time": data.get("lifetime_time", 0.0),
            "lifetime_freq": data.get("lifetime_freq", 0.0),
            "lifetime_natural": data.get("lifetime_natural", 0.0),
            "lifetime_damping": data.get("lifetime_damping", 0.0),
            "average_lifetime": data.get("average_lifetime", 0.0),
            "ai_lifetime": data.get("ai_lifetime", 0.0)
        }
        
        # Include time and acceleration arrays only if new data is available
        if new_data_available:
            response["time"] = data.get("time", [])
            response["acceleration"] = data.get("acceleration", [])
        
        # Set new_data_available to false after retrieval
        if new_data_available:
            data["new_data_available"] = False
            save_data_store(data)
        
        return response
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving data: {str(e)}"
        )

@app.get("/full-refresh")
async def full_refresh():
    """
    Return complete dataset with all metrics
    
    This endpoint returns all arrays and computed metrics for
    initial page load or full refresh scenarios.
    
    Requirements: 12.3
    """
    try:
        # Load current data store
        data = load_data_store()
        
        # Return complete dataset
        return {
            "time": data.get("time", []),
            "acceleration": data.get("acceleration", []),
            "frequency": data.get("frequency", []),
            "amplitude": data.get("amplitude", []),
            "damping_factor": data.get("damping_factor", 0.0),
            "natural_frequency": data.get("natural_frequency", 0.0),
            "lifetime_time": data.get("lifetime_time", 0.0),
            "lifetime_freq": data.get("lifetime_freq", 0.0),
            "lifetime_natural": data.get("lifetime_natural", 0.0),
            "lifetime_damping": data.get("lifetime_damping", 0.0),
            "average_lifetime": data.get("average_lifetime", 0.0),
            "ai_lifetime": data.get("ai_lifetime", 0.0)
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving full dataset: {str(e)}"
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
