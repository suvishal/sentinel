from sqlalchemy.orm import Session
from app import schemas
from app import models
from typing import Optional
from fastapi import Query


def create_log(
    db: Session,
    level: str,
    service: str,
    message: str
):

    log = models.Log(
        level=level,
        service=service,
        message=message
    )

    db.add(log)

    db.commit()

    db.refresh(log)

    return log

def get_logs( db: Session,
    level: Optional[schemas.LogLevel] = None,
    service: Optional[str] = None,
    limit: int = 25,
    offset: int = 0
    ):
    query = db.query(models.Log)

    if level:
        query = query.filter(models.Log.level == level)

    if service:
        query = query.filter(models.Log.service == service)
   
    query = query.offset(offset).limit(limit)

    return query.all()
   

def update_log(
    db: Session,
    log_id: int,
    log_update: schemas.LogUpdate
    ):
   
        db_log = db.query(models.Log).filter(
            models.Log.id == log_id
        ).first()
                
        if db_log is None:
            return None
        db_log.level = log_update.level
        db_log.service = log_update.service
        db_log.message = log_update.message

        db.commit()
        db.refresh(db_log)

        return db_log

def delete_log(
    db: Session,
    log_id: int
    ):
     
        db_log = db.query(models.Log).filter(
                models.Log.id == log_id
        ).first()

        if db_log is None:
            return None

        db.delete(db_log)

        db.commit()

        return True