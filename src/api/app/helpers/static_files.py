from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import os

def setup_static_files(app: FastAPI):
    """
    Configure static files serving for charts and reports
    """
    
    # Define the base static directory
    static_base_dir = "/code/api/static"
    
    # Ensure directories exist
    charts_dir = os.path.join(static_base_dir, "charts")
    reports_dir = os.path.join(static_base_dir, "reports")
    
    os.makedirs(charts_dir, exist_ok=True)
    os.makedirs(reports_dir, exist_ok=True)
    
    # Mount static files directories
    # This will serve files at /static/charts/* and /static/reports/*
    app.mount("/static", StaticFiles(directory=static_base_dir), name="static")
    
    # Alternative: Mount each directory separately if you prefer
    # app.mount("/static/charts", StaticFiles(directory=charts_dir), name="charts")
    # app.mount("/static/reports", StaticFiles(directory=reports_dir), name="reports")
    
    print(f"✅ Static files configured:")
    print(f"   📊 Charts: {charts_dir}")
    print(f"   📄 Reports: {reports_dir}")
    print(f"   🌐 Accessible at: http://localhost:8002/static/")