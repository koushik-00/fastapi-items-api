from database import Base
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship

class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key = True, index=True)
    name = Column(String, nullable=False)
    price = Column(Float, nullable=False)

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)