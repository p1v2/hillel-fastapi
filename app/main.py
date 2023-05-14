import json
from typing import Annotated, Optional

from sqlalchemy.ext.asyncio import async_session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from starlette.status import HTTP_204_NO_CONTENT

from app.dependencies.db import SQLALCHEMY_DATABASE_URL
from app.models import BookCreate, Book, BookUpdate
from app.routers.books import router as books

from fastapi import FastAPI, Response, Header, Cookie, UploadFile, HTTPException, status



app = FastAPI()
app.include_router(
    router=books,
)


# @app.middleware("http")
# async def check_basic_auth(request: Request, call_next):
#     if not request.headers.get("authorization"):
#         return Response(status_code=401, content=json.dumps({"message": "Unauthorized"}))
#     if request.headers.get("authorization") != "Bearer 123":
#         return Response(status_code=403, content=json.dumps({"message": "Forbidden"}))
#
#     return await call_next(request)


@app.get("/")
async def echo(message: str = "Hello World"):
    return {"message": message}


# @app.get("/{message}")
# async def echo_with_url_param(message: str, name: str):
#     return {"message": f"{message} {name}"}


@app.get("/user_agent")
async def get_user_agent(user_agent: Annotated[Optional[str], Header()] = None):
    return {"user_agent": user_agent}


# Getting params from cookies
@app.get("/cookie")
async def get_cookie_or_default(
    tracking: Optional[str] = Cookie(default=None),
):
    response_content = json.dumps({"tracking": tracking})
    response = Response(content=response_content)

    # Set tracking cookies
    response.set_cookie(key="tracking", value="yes")
    return response


# Upload file
@app.post("/upload")
async def upload_file(file: UploadFile):
    return {"size": len(await file.read())}

@app.post("/books")
async def create_book(book: BookCreate):
    async with async_session() as session:
        new_book = Book(title=book.title, author=book.author, pages_count=book.pages_count)
        session.add(new_book)
        await session.commit()
        await session.refresh(new_book)
        return new_book


engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# searching book by id
@app.get("/books/{book_id}")
async def get_book(book_id: int):
    db = SessionLocal()
    book = db.query(Book).filter(Book.id == book_id).first()
    db.close()

    if book is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")

    return {"book_id": book.id, "title": book.title, "author": book.author, "pages_count": book.pages_count}

# updating book by id
@app.put("/books/{book_id}")
async def update_book(book_id: int, book_update: BookUpdate):
    db = SessionLocal()
    book = db.query(Book).filter(Book.id == book_id).first()

    if book is None:
        db.close()
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")


    book.title = book_update.title
    book.author = book_update.author
    book.pages_count = book_update.pages_count

    db.commit()
    db.close()

    return {"message": "Book updated successfully"}

# deleting book by id
@app.delete("/books/delete/{book_id}")
async def delete_book(book_id: int):
    db = SessionLocal()
    book = db.query(Book).filter(Book.id == book_id).first()

    if book is None:
        db.close()
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")

    db.delete(book)
    db.commit()
    db.close()

    return Response(status_code=HTTP_204_NO_CONTENT)
