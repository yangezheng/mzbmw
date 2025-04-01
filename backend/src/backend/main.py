from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
from datasheet_downloader import download_datasheet
import asyncio
import os
import shutil
import glob
import time
from datetime import datetime, timedelta

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # for dev, lock down in prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ensure directories exist
os.makedirs("datasheets", exist_ok=True)
os.makedirs("debug_screenshots", exist_ok=True)

@app.on_event("startup")
async def startup_event():
    # Clean any leftover files on startup
    await cleanup_old_files()
    
    # Start background task for periodic cleanup
    asyncio.create_task(periodic_cleanup())

async def periodic_cleanup():
    """Periodically clean up old files"""
    while True:
        await cleanup_old_files()
        # Run every hour
        await asyncio.sleep(3600)

async def cleanup_old_files():
    """Clean up files older than 24 hours"""
    try:
        print("Running periodic cleanup of old files...")
        now = time.time()
        # 24 hours in seconds
        max_age = 24 * 60 * 60
        
        # Clean datasheets
        for file in glob.glob("datasheets/*.pdf"):
            if os.path.exists(file) and (now - os.path.getmtime(file)) > max_age:
                os.remove(file)
                print(f"Removed old datasheet: {file}")
                
        # Clean debug screenshots
        for file in glob.glob("debug_screenshots/*.png"):
            if os.path.exists(file) and (now - os.path.getmtime(file)) > max_age:
                os.remove(file)
                print(f"Removed old screenshot: {file}")
                
    except Exception as e:
        print(f"Error during periodic cleanup: {str(e)}")

# hello world
@app.get("/")
async def root():
    return {"message": "Hi, Uvicorn is running!"}

class InputData(BaseModel):
    input: float

class DatasheetData(BaseModel):
    MPN: str

# Example of a POST endpoint
@app.post("/api/calculate")
async def calculate(data: InputData):
    try:
        result = data.input * 2
        return {"result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def cleanup_datasheet_files(file_path: str, mpn: str):
    """
    Clean up the downloaded datasheet file and associated debug screenshots
    after they've been served to the user.
    
    Args:
        file_path: Path to the datasheet file that was just served
        mpn: The MPN of the component for finding related debug screenshots
    """
    try:
        # Remove the datasheet file that was just served
        if os.path.exists(file_path):
            os.remove(file_path)
            print(f"Removed datasheet file: {file_path}")
            
        # Remove any debug screenshots for this MPN
        screenshot_pattern = f"debug_screenshots/search_{mpn}_datasheet_filetype:pdf_*.png"
        for screenshot in glob.glob(screenshot_pattern):
            os.remove(screenshot)
            print(f"Removed debug screenshot: {screenshot}")
            
    except Exception as e:
        print(f"Error during cleanup: {str(e)}")

@app.post("/api/download-datasheet")
async def download_datasheet_endpoint(data: DatasheetData, background_tasks: BackgroundTasks):
    try:
        # Run the synchronous function in a separate thread
        file_path = await asyncio.to_thread(
            download_datasheet,
            mpn=data.MPN,
            download_dir="datasheets",
            headless=True
        )
        
        # Check if file exists
        if not os.path.exists(file_path):
            raise HTTPException(status_code=404, detail="Datasheet file not found")
        
        # Schedule cleanup to run after response is sent
        background_tasks.add_task(cleanup_datasheet_files, file_path, data.MPN)
            
        # Return the file as a download response
        return FileResponse(
            path=file_path, 
            filename=os.path.basename(file_path),
            media_type="application/pdf",
            background=background_tasks
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
