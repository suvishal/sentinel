from fastapi import FastAPI
from app.database import engine
from app import models
from fastapi import Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app import crud
from app import schemas
from fastapi import HTTPException
from fastapi import Response
from fastapi import status


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
    
@app.get("/logs")
def get_logs(db: Session = Depends(get_db)):
    return crud.get_logs(db)

@app.put("/logs/{log_id}", response_model=schemas.Log)
def update_log(
    log_id: int,
    log_update: schemas.LogUpdate,
    db: Session = Depends(get_db)
):
    updated_log = crud.update_log(
        db,
        log_id,
        log_update
    )

    if updated_log is None:
        raise HTTPException(
            status_code=404,
            detail="Log not found"
        )

    return updated_log

@app.delete("/logs/{log_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_log(
    log_id: int,
    db: Session = Depends(get_db)
):
    deleted = crud.delete_log(db, log_id)

    if deleted is None:
        raise HTTPException(
            status_code=404,
            detail="Log not found"
        )

    return Response(status_code=status.HTTP_204_NO_CONTENT)

#@app.get("/logs")
#def get_logs():
 #   return logs

