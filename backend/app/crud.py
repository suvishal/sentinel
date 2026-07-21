from sqlalchemy.orm import Session

from app import models


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