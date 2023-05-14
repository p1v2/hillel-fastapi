from pydantic import BaseModel
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    author = Column(String(255), nullable=False)
    pages_count = Column(Integer, nullable=True)


class BookCreate(BaseModel):
    title: str
    author: str
    pages_count: int


class BookUpdate(BaseModel):
    title: str
    author: str
    pages_count: int
