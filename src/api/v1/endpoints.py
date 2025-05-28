from fastapi import HTTPException
from api.v1.schema import Book, BookCreate
from loguru import logger

from fastapi import (
    APIRouter,
)

router = APIRouter(prefix="/books",tags=["Books"])


# Simulated database
books_db: list[Book] = []
counter_id = 0


# Get all books
@router.get("", response_model=list[Book])
async def get_books() -> list[Book]:
    logger.info("Retrieving all books")
    return books_db

@router.post("", response_model=Book, status_code=201)
async def create_book(book: BookCreate) -> Book:
    global counter_id
    counter_id += 1
    new_book = Book(id=counter_id, **book.model_dump())
    books_db.append(new_book)
    logger.info(f"Created new book with ID: {counter_id}")
    return new_book

# Get book by ID
@router.get("/{book_id}", response_model=Book)
async def get_book(book_id: int) -> Book:
    logger.info(f"Retrieving book with ID: {book_id}")
    for book in books_db:
        if book.id == book_id:
            return book
    logger.error(f"Book with ID {book_id} not found")
    raise HTTPException(status_code=404, detail="Book not found")

# Update a book
@router.put("/{book_id}", response_model=Book)
async def update_book(book_id: int, updated: BookCreate) -> Book:
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
@router.delete("/{book_id}", status_code=204)
async def delete_book(book_id: int) -> None:
    logger.info(f"Attempting to delete book with ID: {book_id}")
    for i, book in enumerate(books_db):
        if book.id == book_id:
            books_db.pop(i)
            logger.info(f"Successfully deleted book with ID: {book_id}")
            return
    logger.error(f"Book with ID {book_id} not found for deletion")
    raise HTTPException(status_code=404, detail="Book not found")
