import json

from fastapi import APIRouter, Depends, HTTPException
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


class BookUpdate(BaseModel):
    title: str = None
    author: str = None
    description: str = None
    pages_count: int = None


@router.get("", response_model=list[BookModel])
async def get_books(title: str = None, session=Depends(get_session)):
    books = session.query(Book).all()

    return [BookModel.from_orm(book) for book in books]


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


@router.put("/books/{book_id}", response_model=BookModel, status_code=200)
async def update_book(book_id: int, book_update: BookUpdate, session=Depends(get_session)):
    for var, value in vars(book_update).items():
        if value is not None:
            setattr(book_id, var, value)
    session.commit()
    

@router.delete("/books/{book_id}", response_model=BookModel)
async def delete_book(book_id: int, session=Depends(get_session)):
    book = session.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    session.delete(book)
    session.commit()
    return {"message": "Book deleted"}


@router.get("/books/{book_id}", response_model=BookModel)
async def get_book(book_id: int, session=Depends(get_session)):
    if book := session.query(Book).filter(Book.id == book_id).first():
        return Book(**book.__dict__)
    else:
        raise HTTPException(status_code=404, detail="Book not found")