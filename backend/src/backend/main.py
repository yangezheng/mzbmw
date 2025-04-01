from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

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

# Example of a POST endpoint
@app.post("/api/calculate")
async def calculate(data: InputData):
    try:
        result = data.input * 2
        return {"result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
