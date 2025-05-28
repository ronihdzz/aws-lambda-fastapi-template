from api.v1.schema import Book, BookCreate
from loguru import logger
from shared.base_responses import create_response_for_fast_api,EnvelopeResponse
from core.exceptions import BookException
from fastapi import (
    APIRouter,
)
from fastapi import Response

router = APIRouter(prefix="/books",tags=["Books"])


# Simulated database
books_db: list[Book] = []
counter_id = 0


# Get all books
@router.get("", response_model=EnvelopeResponse)
async def get_books():
    logger.info("Retrieving all books")
    return create_response_for_fast_api(
        data=books_db or None,
        status_code_http=200
    )

# Get all books
@router.get("", response_model=EnvelopeResponse)
async def get_books() -> EnvelopeResponse:
    logger.info("Retrieving all books")
    return create_response_for_fast_api(
        data=books_db,
        status_code_http=200
    )

@router.post("", response_model=EnvelopeResponse)
async def create_book(book: BookCreate) -> EnvelopeResponse:
    global counter_id
    counter_id += 1
    new_book = Book(id=counter_id, **book.model_dump())
    books_db.append(new_book)
    logger.info(f"Created new book with ID: {counter_id}")
    return create_response_for_fast_api(
        data=new_book,
        status_code_http=201
    )

# Get book by ID
@router.get("/{book_id}", response_model=EnvelopeResponse)
async def get_book(book_id: int) -> EnvelopeResponse:
    logger.info(f"Retrieving book with ID: {book_id}")
    for book in books_db:
        if book.id == book_id:
            return create_response_for_fast_api(
                data=book,
                status_code_http=201
            )
    logger.error(f"Book with ID {book_id} not found")
    raise BookException(
        message=f"Book with ID {book_id} not found",
        data={
            "payload": {
                "book_id": book_id
            }
        }
    )

# Update a book
@router.put("/{book_id}", response_model=EnvelopeResponse)
async def update_book(book_id: int, updated: BookCreate) -> EnvelopeResponse:
    logger.info(f"Attempting to update book with ID: {book_id}")
    for i, book in enumerate(books_db):
        if book.id == book_id:
            updated_book = Book(id=book_id, **updated.model_dump())
            books_db[i] = updated_book
            logger.info(f"Successfully updated book with ID: {book_id}")
            return create_response_for_fast_api(
                data=updated_book,
                status_code_http=200
            )
    logger.error(f"Book with ID {book_id} not found for update")
    raise BookException(
        message=f"Book with ID {book_id} not found for update",
        data={
            "payload": {
                "book_id": book_id
            }
        }
    )
# Delete a book
@router.delete("/{book_id}", status_code=204)
async def delete_book(book_id: int) -> None:
    logger.info(f"Attempting to delete book with ID: {book_id}")
    for i, book in enumerate(books_db):
        if book.id == book_id:
            books_db.pop(i)
            logger.info(f"Successfully deleted book with ID: {book_id}")
            return Response(status_code=204)
    logger.error(f"Book with ID {book_id} not found for deletion")
    raise BookException(
        message=f"Book with ID {book_id} not found for deletion",
        data={
            "payload": {
                "book_id": book_id
            }
        }
    )