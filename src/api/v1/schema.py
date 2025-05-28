from pydantic import BaseModel
from db.posgresql.models.public import BookType
from uuid import UUID

# Data model
class BookSchema(BaseModel):
    id: UUID
    title: str
    author: str
    year: int
    type: BookType

    class Config:
        allow_population_by_field_name = False
        json_encoders = {
            UUID: lambda v: str(v),
        }

# Create a new book
class BookCreateSchema(BaseModel):
    title: str
    author: str
    year: int
    type: BookType