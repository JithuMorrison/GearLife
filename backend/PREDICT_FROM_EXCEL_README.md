# 📊 Predicting Lifetime from Real Excel Data

This guide shows you how to use your real acceleration data from an Excel file to predict equipment lifetime.

---

## 📋 Prerequisites

1. **Install additional dependencies:**

   ```bash
   cd backend

   # Activate virtual environment
   # Windows:
   venv\Scripts\activate
   # Mac/Linux:
   source venv/bin/activate

   # Install pandas and openpyxl
   pip install pandas openpyxl
   ```

2. **Your Excel file should contain:**
   - Column 1: Time (seconds) OR just row numbers
   - Column 2: Acceleration values (m/s²)

   Example:

   ```
   Time (s)    Acceleration (m/s²)
   0.000       0.123
   0.001       0.456
   0.002       0.789
   ...
   ```

---

## 🚀 How to Run

### Step 1: Place Your Excel File

Make sure your Excel file is in the project root directory:

```
your-project/
├── acceleration data_669853.tmp.xlsx  ← Your file here
├── backend/
│   ├── predict_from_excel.py
│   └── ...
```

### Step 2: Run the Prediction Script

```bash
cd backend

# Activate virtual environment if not already active
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Run the script
python predict_from_excel.py
```

---

## 📈 What the Script Does

The script will:

1. **Load your Excel data**
   - Reads time and acceleration columns
   - Validates and cleans the data
   - Shows data statistics

2. **Perform FFT Analysis**
   - Converts time-domain signal to frequency-domain
   - Identifies frequency components

3. **Calculate Damping Factor**
   - Uses logarithmic decrement method
   - Classifies as NORMAL/WARNING/CRITICAL

4. **Detect Natural Frequency**
   - Finds dominant frequency peak
   - Compares with baseline (50 Hz)

5. **Calculate 4 Lifetime Estimates**
   - Time-domain (exponential decay)
   - Frequency-domain (spectral energy)
   - Natural frequency shift
   - Damping-based

6. **Compute Weighted Average**
   - Combines all 4 estimates equally

7. **AI Model Prediction**
   - Uses machine learning model
   - Compares with traditional methods

8. **Save Results**
   - Creates `real_data_analysis_results.json`
   - Contains all computed metrics

---

## 📊 Example Output

```
Loading data from ../acceleration data_669853.tmp.xlsx...
Excel file loaded successfully!
Columns found: ['Time', 'Acceleration']
Shape: (10000, 2)

Data loaded successfully!
Time range: 0.0000 to 9.9990 seconds
Acceleration range: -15.2341 to 18.4567 m/s²
Number of samples: 10000

============================================================
VIBRATION ANALYSIS RESULTS
============================================================

1. Computing FFT...
   ✓ FFT computed: 5001 frequency bins

2. Calculating damping factor...
   ✓ Damping factor: 0.0523
   Status: NORMAL (low damping)

3. Detecting natural frequency...
   ✓ Natural frequency: 52.34 Hz
   Shift from baseline (50 Hz): 2.34 Hz
   Status: NORMAL (within baseline range)

4. Calculating lifetime estimates...
   ✓ Time-domain lifetime: 1234.5 hours
   ✓ Frequency-domain lifetime: 1456.7 hours
   ✓ Natural frequency shift lifetime: 2345.6 hours
   ✓ Damping-based lifetime: 1890.2 hours

5. Calculating weighted average lifetime...
   ✓ Weighted average lifetime: 1731.8 hours

6. AI model prediction...
   ✓ AI predicted lifetime: 1650.3 hours
   Difference from average: 4.7%
   Status: GOOD AGREEMENT

✓ Results saved to real_data_analysis_results.json

============================================================
SUMMARY
============================================================
Damping Factor:        0.0523
Natural Frequency:     52.34 Hz
Time-Domain Lifetime:  1234.5 hours
Freq-Domain Lifetime:  1456.7 hours
Natural Freq Lifetime: 2345.6 hours
Damping Lifetime:      1890.2 hours
Average Lifetime:      1731.8 hours
AI Predicted Lifetime: 1650.3 hours
============================================================

Lifetime in days: 72.2 days
AI prediction in days: 68.8 days
```

---

## 📁 Output Files

After running, you'll get:

1. **real_data_analysis_results.json**
   - Complete analysis results
   - All computed metrics
   - Frequency and amplitude arrays
   - Can be used for further analysis

---

## 🔧 Customization

### Change Sampling Rate

If your data doesn't have a time column, the script assumes 1000 Hz. To change:

Edit `predict_from_excel.py`, line ~40:

```python
sampling_rate = 1000.0  # Change this value
```

### Change Baseline Frequency

To change the baseline natural frequency (default 50 Hz):

Edit `predict_from_excel.py`, line ~130:

```python
baseline_freq = 50.0  # Change this value
```

### Use Different Excel File

Edit `predict_from_excel.py`, line ~220:

```python
excel_file = "../your_file_name.xlsx"
```

---

## 🎯 Interpreting Results

### Damping Factor

- **0.00 - 0.10**: NORMAL (healthy system)
- **0.10 - 0.20**: WARNING (increased wear)
- **> 0.20**: CRITICAL (significant degradation)

### Natural Frequency Shift

- **< 5 Hz shift**: NORMAL
- **5 - 10 Hz shift**: WARNING
- **> 10 Hz shift**: CRITICAL

### Lifetime Estimates

- **> 2000 hours**: Excellent condition
- **1000 - 2000 hours**: Good condition
- **500 - 1000 hours**: Fair condition (plan maintenance)
- **< 500 hours**: Poor condition (urgent maintenance)

### AI vs Average Agreement

- **< 10% difference**: GOOD AGREEMENT
- **10 - 20% difference**: MODERATE AGREEMENT
- **> 20% difference**: SIGNIFICANT DIVERGENCE (investigate)

---

## ❓ Troubleshooting

**Error: "No module named 'pandas'"**

```bash
pip install pandas openpyxl
```

**Error: "File not found"**

- Check the file path in the script
- Make sure Excel file is in the correct location

**Error: "Invalid Excel file"**

- Make sure file is .xlsx format (not .xls)
- Try opening in Excel and re-saving

**Unexpected results:**

- Check your data units (should be m/s²)
- Verify time column is in seconds
- Look for data quality issues (NaN, outliers)

---

## 🔄 Next Steps

After getting predictions:

1. **Compare with historical data** - Is this consistent with past measurements?
2. **Trend analysis** - Run periodically to track degradation
3. **Maintenance planning** - Schedule based on predicted lifetime
4. **Model improvement** - Collect actual failure data to retrain AI model

---

## 📞 Need Help?

If you encounter issues:

1. Check the console output for error messages
2. Verify your Excel file format
3. Ensure all dependencies are installed
4. Check that virtual environment is activated
