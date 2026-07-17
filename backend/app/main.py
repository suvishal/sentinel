from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

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
    return {
        "status": "received",
        "log": log
    }