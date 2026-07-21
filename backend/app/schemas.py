from pydantic import BaseModel


class LogCreate(BaseModel):
    level: str
    service: str
    message: str