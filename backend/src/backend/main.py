from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel
from datasheet_downloader import download_datasheet
import asyncio
import os
import shutil
import glob
import time
import subprocess
import logging
from datetime import datetime, timedelta

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("datasheet_download.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

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

# Check if we're running on Render
ON_RENDER = os.environ.get("RENDER", "false").lower() == "true"

@app.on_event("startup")
async def startup_event():
    # Clean any leftover files on startup
    await cleanup_old_files()
    
    # Start background task for periodic cleanup
    asyncio.create_task(periodic_cleanup())
    
    # Ensure Playwright is installed correctly
    if ON_RENDER:
        try:
            logger.info("Running on Render - checking Playwright installation")
            # Try to install browser if not already installed
            result = subprocess.run(
                ["python", "-m", "playwright", "install", "chromium"],
                capture_output=True,
                text=True
            )
            logger.info(f"Playwright install result: {result.stdout}")
            if result.returncode != 0:
                logger.error(f"Playwright install error: {result.stderr}")
                
            # Check browser path
            browser_path = "/tmp/playwright-browsers"
            if not os.path.exists(browser_path):
                logger.warning(f"Browser path {browser_path} does not exist, creating it")
                os.makedirs(browser_path, exist_ok=True)
                os.chmod(browser_path, 0o777)
        except Exception as e:
            logger.error(f"Error setting up Playwright: {str(e)}")

async def periodic_cleanup():
    """Periodically clean up old files"""
    while True:
        await cleanup_old_files()
        # Run every hour
        await asyncio.sleep(3600)

async def cleanup_old_files():
    """Clean up files older than 24 hours"""
    try:
        logger.info("Running periodic cleanup of old files...")
        now = time.time()
        # 24 hours in seconds
        max_age = 24 * 60 * 60
        
        # Clean datasheets
        for file in glob.glob("datasheets/*.pdf"):
            if os.path.exists(file) and (now - os.path.getmtime(file)) > max_age:
                os.remove(file)
                logger.info(f"Removed old datasheet: {file}")
                
        # Clean debug screenshots
        for file in glob.glob("debug_screenshots/*.png"):
            if os.path.exists(file) and (now - os.path.getmtime(file)) > max_age:
                os.remove(file)
                logger.info(f"Removed old screenshot: {file}")
                
    except Exception as e:
        logger.error(f"Error during periodic cleanup: {str(e)}")

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
        logger.error(f"Calculate error: {str(e)}")
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
            logger.info(f"Removed datasheet file: {file_path}")
            
        # Remove any debug screenshots for this MPN
        screenshot_pattern = f"debug_screenshots/search_{mpn}_datasheet_filetype:pdf_*.png"
        for screenshot in glob.glob(screenshot_pattern):
            os.remove(screenshot)
            logger.info(f"Removed debug screenshot: {screenshot}")
            
    except Exception as e:
        logger.error(f"Error during cleanup: {str(e)}")

@app.post("/api/download-datasheet")
async def download_datasheet_endpoint(data: DatasheetData, background_tasks: BackgroundTasks):
    try:
        logger.info(f"Downloading datasheet for MPN: {data.MPN}")
        
        # Try to ensure Playwright browsers are installed
        if ON_RENDER:
            try:
                # Ensure browsers are installed before proceeding
                subprocess.run(
                    ["python", "-m", "playwright", "install", "chromium"],
                    check=True,
                    capture_output=True
                )
                logger.info("Playwright browser installation verified")
            except subprocess.CalledProcessError as e:
                logger.error(f"Failed to install Playwright browser: {e.stderr}")
                return JSONResponse(
                    status_code=500,
                    content={"detail": f"Browser installation error: {e.stderr.decode() if hasattr(e.stderr, 'decode') else str(e.stderr)}"}
                )
        
        # Run the synchronous function in a separate thread
        file_path = await asyncio.to_thread(
            download_datasheet,
            mpn=data.MPN,
            download_dir="datasheets",
            headless=True
        )
        
        logger.info(f"Datasheet downloaded to: {file_path}")
        
        # Check if file exists
        if not os.path.exists(file_path):
            logger.error(f"Datasheet file not found: {file_path}")
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
        logger.error(f"Download datasheet error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
