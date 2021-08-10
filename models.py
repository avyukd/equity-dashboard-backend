from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from .database import Base

class Watchlist(Base):
    __tablename__ = "watchlist"

    ticker = Column(String(10), primary_key=True, index=True)
    name = Column(String(50), unique=True)