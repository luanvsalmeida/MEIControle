# api/config/static_files.py
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pathlib import Path

def setup_static_files(app: FastAPI) -> None:
    """
    Setup static file serving for charts and reports
    
    Args:
        app: FastAPI application instance
    """
    
    # Get base directory (assuming this file is in api/config/)
    base_dir = Path(__file__).resolve().parent.parent
    
    # Setup static directories
    static_dir = base_dir / "static"
    charts_dir = static_dir / "charts"
    reports_dir = static_dir / "reports"
    
    # Create directories if they don't exist
    charts_dir.mkdir(parents=True, exist_ok=True)
    reports_dir.mkdir(parents=True, exist_ok=True)
    
    # Mount static file directories
    app.mount("/static/charts", StaticFiles(directory=str(charts_dir)), name="charts")
    app.mount("/static/reports", StaticFiles(directory=str(reports_dir)), name="reports")
    app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")
    
    print(f"Static files configured:")
    print(f"  Charts: {charts_dir}")
    print(f"  Reports: {reports_dir}")

