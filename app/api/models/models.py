from app.api.database import Base
from sqlalchemy import Column, DateTime, Integer, String
from datetime import datetime

class RequestHistory(Base):
    __tablename__ = "request_history"
    id = Column(Integer, primary_key=True, index=True)
    address = Column(String(34))
    created_at = Column(DateTime, default=datetime.now())
