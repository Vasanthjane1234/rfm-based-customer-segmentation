#!/usr/bin/env python3
"""
Run the Plotly Dash Customer Segmentation Dashboard
"""

import os
import sys
import subprocess

def check_requirements():
    """Check if required packages are installed"""
    required_packages = [
        'dash',
        'plotly', 
        'pandas',
        'numpy',
        'scikit-learn'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"Missing packages: {', '.join(missing_packages)}")
        print("Installing missing packages...")
        subprocess.check_call([sys.executable, '-m', 'pip', 'install'] + missing_packages)
        print("Installation complete!")
    
    return len(missing_packages) == 0

def main():
    """Main function to run the dashboard"""
    print("Customer Segmentation Dashboard")
    print("=" * 40)
    
    # Check if data file exists
    if not os.path.exists('rfm_segments_output.csv'):
        print("Error: rfm_segments_output.csv not found!")
        print("Please run the Jupyter notebook first to generate the RFM data.")
        return
    
    # Check requirements
    print("Checking requirements...")
    check_requirements()
    
    print("\nStarting Dashboard...")
    print("Dashboard will be available at: http://localhost:8050")
    print("Press Ctrl+C to stop the server")
    print("-" * 40)
    
    # Import and run the dashboard
    try:
        from dash_dashboard import app
        app.run(debug=True, host='0.0.0.0', port=8050)
    except ImportError as e:
        print(f"Import error: {e}")
        print("Please ensure all dependencies are installed.")
    except Exception as e:
        print(f"Error running dashboard: {e}")

if __name__ == "__main__":
    main()
