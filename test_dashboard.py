#!/usr/bin/env python3
"""
Test script for the Plotly Dash Customer Segmentation Dashboard
"""

import sys
import os

def test_imports():
    """Test if all required modules can be imported"""
    try:
        import dash
        import plotly.express as px
        import plotly.graph_objects as go
        import pandas as pd
        import numpy as np
        print("✅ All required modules imported successfully")
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def test_data_file():
    """Test if the required data file exists and is readable"""
    try:
        import pandas as pd
        rfm = pd.read_csv('rfm_segments_output.csv')
        print(f"✅ Data file loaded successfully: {len(rfm)} records")
        print(f"   Columns: {list(rfm.columns)}")
        print(f"   Segments: {rfm['segment'].unique()}")
        print(f"   Clusters: {sorted(rfm['cluster'].unique())}")
        return True
    except FileNotFoundError:
        print("❌ Data file 'rfm_segments_output.csv' not found")
        return False
    except Exception as e:
        print(f"❌ Error reading data file: {e}")
        return False

def test_dashboard_creation():
    """Test if the dashboard can be created without errors"""
    try:
        from dash_dashboard import app
        print("✅ Dashboard app created successfully")
        print(f"   App title: {app.title}")
        return True
    except Exception as e:
        print(f"❌ Error creating dashboard: {e}")
        return False

def test_plotly_charts():
    """Test if basic Plotly charts can be created"""
    try:
        import plotly.express as px
        import pandas as pd
        
        # Load data
        rfm = pd.read_csv('rfm_segments_output.csv')
        
        # Test bar chart
        fig = px.bar(x=rfm['segment'].value_counts().index, 
                    y=rfm['segment'].value_counts().values,
                    title="Test Chart")
        print("✅ Plotly bar chart created successfully")
        
        # Test scatter plot
        fig = px.scatter(rfm, x='recency', y='frequency', 
                        title="Test Scatter")
        print("✅ Plotly scatter plot created successfully")
        
        return True
    except Exception as e:
        print(f"❌ Error creating Plotly charts: {e}")
        return False

def main():
    """Run all tests"""
    print("Customer Segmentation Dashboard - Test Suite")
    print("=" * 50)
    
    tests = [
        ("Module Imports", test_imports),
        ("Data File", test_data_file),
        ("Dashboard Creation", test_dashboard_creation),
        ("Plotly Charts", test_plotly_charts)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n🧪 Testing: {test_name}")
        if test_func():
            passed += 1
        else:
            print(f"   Test failed: {test_name}")
    
    print("\n" + "=" * 50)
    print(f"Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Dashboard is ready to run.")
        print("\nTo start the dashboard, run:")
        print("   python dash_dashboard.py")
        print("   or")
        print("   python run_dash.py")
    else:
        print("❌ Some tests failed. Please check the errors above.")
        return False
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
