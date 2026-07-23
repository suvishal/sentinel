from fastapi import FastAPI
from app.database import engine
from app import models
from fastapi import Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app import crud
from app import schemas

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


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
def receive_log(
    log: schemas.LogCreate,
    db: Session = Depends(get_db)
):
    return crud.create_log(
        db=db,
        level=log.level,
        service=log.service,
        message=log.message
    )
    

#@app.get("/logs")
#def get_logs():
 #   return logs

