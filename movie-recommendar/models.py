from sqlalchemy import create_engine,Column,Integer,String,Float,Text,DateTime
from database import Base
from datetime import datetime

class Movie(Base):
    __tablename__ = "movies"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    genre = Column(String)
    year = Column(Integer)
    rating = Column(Float)
    description = Column(Text)
    poster_url = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
