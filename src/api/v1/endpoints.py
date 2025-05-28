from api.v1.schema import BookSchema, BookCreateSchema
from loguru import logger
from shared.base_responses import create_response_for_fast_api, EnvelopeResponse
from core.exceptions import BookException
from fastapi import APIRouter, Response
from api.v1.repositories import BookRepository
from uuid import UUID

router = APIRouter(prefix="/books", tags=["Books"])


@router.get("", response_model=EnvelopeResponse)
async def get_books() -> EnvelopeResponse:
    logger.info("Retrieving all books")
    success, list_books = BookRepository.get_all()
    list_books_schema = [BookSchema(**book.to_dict()) for book in list_books]
    return create_response_for_fast_api(data=list_books_schema if success else None)


@router.post("", response_model=EnvelopeResponse)
async def create_book(book: BookCreateSchema) -> EnvelopeResponse:
    logger.info("Creating new book")
    success, new_book = BookRepository.create(book)
    if not success:
        logger.error("Book creation failed")
        raise BookException(message="Failed to create book")
    logger.info(f"Book created with ID: {new_book.id}")
    return create_response_for_fast_api(data=BookSchema(**new_book.to_dict()), status_code_http=201)


@router.get("/{book_id}", response_model=EnvelopeResponse)
async def get_book(book_id: UUID) -> EnvelopeResponse:
    logger.info(f"Retrieving book with ID: {book_id}")
    success, book = BookRepository.get_by_id(book_id)
    if not success:
        logger.error(f"Book with ID {book_id} not found")
        raise BookException(
            message=f"Book with ID {book_id} not found",
            data={"payload": {"book_id": str(book_id)}}
        )
    return create_response_for_fast_api(data=BookSchema(**book.to_dict()))


@router.put("/{book_id}", response_model=EnvelopeResponse)
async def update_book(book_id: UUID, updated: BookCreateSchema) -> EnvelopeResponse:
    logger.info(f"Updating book with ID: {book_id}")
    success, updated_book = BookRepository.update(book_id, updated)
    if not success:
        logger.error(f"Book with ID {book_id} not found for update")
        raise BookException(
            message=f"Book with ID {book_id} not found for update",
            data={"payload": {"book_id": str(book_id)}}
        )
    logger.info(f"Successfully updated book with ID: {book_id}")
    return create_response_for_fast_api(data=BookSchema(**updated_book.to_dict()))


@router.delete("/{book_id}", status_code=204)
async def delete_book(book_id: UUID) -> None:
    logger.info(f"Attempting to delete book with ID: {book_id}")
    success, _ = BookRepository.delete(book_id)
    if not success:
        logger.error(f"Book with ID {book_id} not found for deletion")
        raise BookException(
            message=f"Book with ID {book_id} not found for deletion",
            data={"payload": {"book_id": str(book_id)}}
        )
    logger.info(f"Successfully deleted book with ID: {book_id}")
    return Response(status_code=204)
