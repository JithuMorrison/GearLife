# 🚀 Quick Start: Using Your Real Acceleration Data

## 📝 Summary

I've created a script that will analyze your real acceleration data from the Excel file and predict equipment lifetime using the same algorithms and AI model that the web application uses.

---

## ⚡ Quick Steps

### 1. Install Dependencies

```bash
cd backend
venv\Scripts\activate
pip install pandas openpyxl
```

### 2. Run the Analysis

```bash
python predict_from_excel.py
```

That's it! The script will:

- ✅ Load your Excel file (`acceleration data_669853.tmp.xlsx`)
- ✅ Perform FFT analysis
- ✅ Calculate damping factor
- ✅ Detect natural frequency
- ✅ Compute 4 different lifetime estimates
- ✅ Use AI model to predict lifetime
- ✅ Save results to JSON file
- ✅ Display comprehensive analysis report

---

## 📊 What You'll Get

### Console Output

```
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

### Output File

- `backend/real_data_analysis_results.json` - Complete analysis data

---

## 📖 Full Documentation

See `backend/PREDICT_FROM_EXCEL_README.md` for:

- Detailed explanation of each step
- How to interpret results
- Customization options
- Troubleshooting guide

---

## 🎯 Key Features

1. **Automatic Data Loading** - Handles various Excel formats
2. **Complete Analysis** - Same algorithms as the web app
3. **AI Prediction** - Uses trained machine learning model
4. **Status Classification** - NORMAL/WARNING/CRITICAL indicators
5. **JSON Export** - Results saved for further analysis
6. **Human-Readable Output** - Clear console display

---

## 💡 Tips

- Your Excel file should have time and acceleration columns
- If only acceleration data exists, script assumes 1000 Hz sampling
- Results are saved to `real_data_analysis_results.json`
- Run periodically to track equipment degradation over time

---

## 🔄 Integration with Web App

The script uses the same backend code as the web application:

- Same signal processing algorithms
- Same lifetime calculation methods
- Same AI model
- Consistent results

You can compare the script output with the web dashboard to verify consistency!
