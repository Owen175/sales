from sqlalchemy import Column, DateTime, Integer, String, Float, ARRAY
from sqlalchemy.orm import declarative_base
from sqlalchemy.sql import func



Base = declarative_base()


class Item(Base):
    __tablename__ = 'items'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    seller = Column(String)
    price = Column(Float)
    content = Column(String)
    keywords = Column(ARRAY(String), nullable=False)
    time_created = Column(DateTime(timezone=True), server_default=func.now())

