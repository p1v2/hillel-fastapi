from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from starlette import status
from sqlalchemy.exc import SQLAlchemyError
from app.dependencies.db import get_session
from app.models import Book

router = APIRouter(prefix="/books")

# books = [
#     {"id": 1, "title": "The Great Gatsby", "author": "vitalii"},
#     {"id": 2, "title": "The DaVinci Code", "author": "not vitalii"},
# ]


class BookModel(BaseModel):
    id: int = None
    title: str = None
    author: str = None
    pages_count: int = None

    class Config:
        orm_mode = True


class BookCreateModel(BaseModel):
    title: str
    author: str


@router.get("", response_model=list[BookModel])
async def get_books(title: str = None, session=Depends(get_session)):
    books = session.query(Book).all()

    books_models = []
    for book in books:
        books_models.append(BookModel.from_orm(book))
    return books_models


# @router.get("/{book_id", response_model=BookModel)
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


@router.patch("/{book_id}", response_model=BookModel, status_code=200)
async def update_book(book_id: int, book: BookCreateModel, session=Depends(get_session)):
    book = Book(**book.dict(exclude_unset=True))
    try:
        item = session.query(Book).filter(Book.id == book_id).first()
    except SQLAlchemyError as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Error while working with database",
        )
    else:
        if item:
            item.title = book.title
            item.author = book.author
            session.commit()
            return BookModel.from_orm(item)
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Book {book_id} does not exist in database",
            )


@router.delete("/{book_id}", response_model=BookModel, status_code=204)
async def delete_book(book_id: int, session=Depends(get_session)):
    try:
        item = session.query(Book).filter(Book.id == book_id).first()
    except SQLAlchemyError as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Error while working with database",
        )
    else:
        if item:
            session.delete(item)
            session.commit()
            return {"message": f"Book {book_id} deleted successfully"}
        else:
            raise HTTPException(
                status_code=status.HTTP_204_NO_CONTENT,
                detail=f"Book {book_id} does not exist in database",
            )


@router.get("/{book_id}", response_model=BookModel, status_code=201)
def find_book(book_id: int, session=Depends(get_session)):
    try:
        item = session.query(Book).filter(Book.id == book_id).first()
        print(item)
        session.commit()
    except SQLAlchemyError as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Error while working with database",
        )
    else:
        if item:
            return BookModel.from_orm(item)
        else:
            raise HTTPException(
                status_code=status.HTTP_204_NO_CONTENT,
                detail=f"Book {book_id} does not exist in database",
            )
