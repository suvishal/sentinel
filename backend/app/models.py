from sqlalchemy import Column, Integer, String
from sqlalchemy import DateTime
from app.database import Base


class Log(Base):
    __tablename__ = "logs"
    
    id = Column(Integer, primary_key=True, index=True)

    level = Column(String, nullable=False)

    service = Column(String, nullable=False)

    message = Column(String, nullable=False)

    timestamp = Column(DateTime)
    
    request_id = Column(String, index=True)