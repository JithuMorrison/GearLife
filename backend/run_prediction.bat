@echo off
echo ============================================================
echo  Vibration Lifetime Prediction - Real Data Analysis
echo ============================================================
echo.

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Check if pandas is installed
python -c "import pandas" 2>nul
if errorlevel 1 (
    echo.
    echo Installing required packages: pandas and openpyxl...
    pip install pandas openpyxl
    echo.
)

REM Run the prediction script
echo.
echo Running analysis on your acceleration data...
echo.
python predict_from_excel.py

echo.
echo ============================================================
echo Analysis complete!
echo Results saved to: real_data_analysis_results.json
echo ============================================================
echo.
pause
