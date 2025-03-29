from pydantic import BaseModel

# Data model
class Book(BaseModel):
    id: int
    title: str
    author: str
    year: int


# Create a new book
class BookCreate(BaseModel):
    title: str
    author: str
    year: int