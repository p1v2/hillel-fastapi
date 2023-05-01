import json

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from app.dependencies.db import get_session
from app.models import Book

router = APIRouter(prefix="/books")

# books = [
#     {"id": 1, "title": "The Great Gatsby", "author": "vitalii"},
#     {"id": 2, "title": "The DaVinci Code", "author": "not vitalii"},
# ]


class BookModel(BaseModel):
    id: int
    title: str
    author: str
    pages_count: int = None

    class Config:
        orm_mode = True


class BookCreateModel(BaseModel):
    title: str
    author: str


@router.get("", response_model=list[BookModel])
async def get_books(title: str = None, session=Depends(get_session)):
    async with session() as session:
        books = await session.query(Book).all()

        books_models = []
        for book in books:
            books_models.append(BookModel.from_orm(book))
        return books_models


# @router.get("/{book_id}", response_model=BookModel)
# async def get_book(book_id: int):
#     try:
#         return next(book for book in books if book["id"] == book_id)
#     except StopIteration:
#         return Response(status_code=404, content=json.dumps({"message": "Book not found"}))


@router.post("", response_model=BookModel, status_code=201)
async def create_book(book: BookCreateModel, session=Depends(get_session)):
    book = Book(**book.dict())

    session.add(book)
    session.commit()
    session.refresh(book)

    return BookModel.from_orm(book)

