from fastapi import FastAPI
from pydantic import BaseModel
from app.database import engine
from app import models

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

logs = []

class Log(BaseModel):
    level: str
    service: str
    message: str


@app.get("/")
def root():
    return {
        "message": "Welcome to Sentinel"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


@app.get("/version")
def version():
    return {
        "version": "0.1.0"
    }

@app.post("/logs")
def receive_log(log: Log):
    
    logs.append(log)
    
    return {
        "status": "stored",
        "total_log": len(logs)
    }

@app.get("/logs")
def get_logs():
    return logs

