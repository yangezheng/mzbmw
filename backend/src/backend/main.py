from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
from datasheet_downloader import download_datasheet
import asyncio
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # for dev, lock down in prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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

@app.post("/api/download-datasheet")
async def download_datasheet_endpoint(data: DatasheetData):
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
            
        # Return the file as a download response
        return FileResponse(
            path=file_path, 
            filename=os.path.basename(file_path),
            media_type="application/pdf"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
