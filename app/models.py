from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    author = Column(String(255), nullable=False)
    pages_count = Column(Integer, nullable=True)


# Список книжок (мокові дані)
books = [
    Book(id=1, title="Book 1", author="Author 1", pages_count = 'pages_count1'),
    Book(id=2, title="Book 2", author="Author 2", pages_count = 'pages_count2'),
    Book(id=3, title="Book 3", author="Author 3", pages_count = 'pages_count3'),
]


# Оновлення книжки за id
@app.put("/books/{id}")
async def update_book(id: int, book: Book):
    for i in range(len(books)):
        if books[i].id == id:
            books[i] = book
            return {"message": "Book updated"}
    raise HTTPException(status_code=404, detail="Book not found")


# Видалення книжки за id
@app.delete("/books/{id}")
async def delete_book(id: int):
    for i in range(len(books)):
        if books[i].id == id:
            del books[i]
            return {"message": "Book deleted"}
    raise HTTPException(status_code=404, detail="Book not found")


# Пошук книжки за id
@app.get("/books/{id}")
async def get_book(id: int):
    for book in books:
        if book.id == id:
            return book
    raise HTTPException(status_code=404, detail="Book not found")