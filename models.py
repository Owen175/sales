from sqlalchemy import Column, DateTime, Integer, String, Float, ARRAY, ForeignKey
from sqlalchemy.orm import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()


class Item(Base):
    __tablename__ = 'items'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    seller = Column(Integer, ForeignKey('users.uid', ondelete='Cascade'), nullable=False)
    price = Column(Float, nullable=False)
    content = Column(String)
    keywords = Column(ARRAY(String), nullable=False)
    time_created = Column(DateTime(timezone=True), server_default=func.now())


class User(Base):
    __tablename__ = 'users'
    uid = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    time_created = Column(DateTime(timezone=True), server_default=func.now())
