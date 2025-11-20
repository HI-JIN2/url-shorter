from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base
from datetime import datetime

Base = declarative_base()

class ShortURL(Base):
    __tablename__ = "short_urls"

    id = Column(Integer, primary_key=True, autoincrement=True)
    short_code = Column(String(16), unique=True, index=True, nullable=False)
    original_url = Column(String(2048), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    hit_count = Column(Integer, default=0)
