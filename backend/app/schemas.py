from enum import Enum
from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional


class LogLevel(str, Enum):
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


class LogCreate(BaseModel):
    level: LogLevel
    service: str = Field(..., min_length=1, max_length=100)
    message: str = Field(..., min_length=1)
    

class LogUpdate(BaseModel):
    level: LogLevel
    service: str = Field(..., min_length=1, max_length=100)
    message: str = Field(..., min_length=1)
    

class Log(LogCreate):
    id: int
    timestamp: Optional[datetime] = None
    class Config:
        from_attributes = True