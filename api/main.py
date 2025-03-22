from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from mangum import Mangum
from fastapi.openapi.utils import get_openapi
from loguru import logger
import os


app = FastAPI(root_path=os.getenv("ROOT_PATH",""))


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Books API",
        version="1.0.0",
        description="A sample API for books",
        routes=app.routes,
    )
    openapi_schema["openapi"] = "3.0.3"  # 👈 force compatible version
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi



# Modelo de datos
class Book(BaseModel):
    id: int
    title: str
    author: str
    year: int

# Base de datos simulada
books_db: List[Book] = []
counter_id = 0

# Root endpoint
@app.get("/")
async def read_root():
    logger.info("Accessing root endpoint")
    return {"message": "Books API 📚"}

# Get all books
@app.get("/books", response_model=List[Book])
async def get_books():
    logger.info("Retrieving all books")
    return books_db

# Get book by ID
@app.get("/books/{book_id}", response_model=Book)
async def get_book(book_id: int):
    logger.info(f"Retrieving book with ID: {book_id}")
    for book in books_db:
        if book.id == book_id:
            return book
    logger.error(f"Book with ID {book_id} not found")
    raise HTTPException(status_code=404, detail="Book not found")

# Create a new book
class BookCreate(BaseModel):
    title: str
    author: str
    year: int

@app.post("/books", response_model=Book, status_code=201)
async def create_book(book: BookCreate):
    global counter_id
    counter_id += 1
    new_book = Book(id=counter_id, **book.model_dump())
    books_db.append(new_book)
    logger.info(f"Created new book with ID: {counter_id}")
    return new_book

# Update a book
@app.put("/books/{book_id}", response_model=Book)
async def update_book(book_id: int, updated: BookCreate):
    logger.info(f"Attempting to update book with ID: {book_id}")
    for i, book in enumerate(books_db):
        if book.id == book_id:
            updated_book = Book(id=book_id, **updated.model_dump())
            books_db[i] = updated_book
            logger.info(f"Successfully updated book with ID: {book_id}")
            return updated_book
    logger.error(f"Book with ID {book_id} not found for update")
    raise HTTPException(status_code=404, detail="Book not found")

# Delete a book
@app.delete("/books/{book_id}", status_code=204)
async def delete_book(book_id: int):
    logger.info(f"Attempting to delete book with ID: {book_id}")
    for i, book in enumerate(books_db):
        if book.id == book_id:
            books_db.pop(i)
            logger.info(f"Successfully deleted book with ID: {book_id}")
            return
    logger.error(f"Book with ID {book_id} not found for deletion")
    raise HTTPException(status_code=404, detail="Book not found")

# Para AWS Lambda
handler = Mangum(app)
