from pydantic import BaseModel

class BookCreate(BaseModel):
    name: str
    author_id: int

class BookUpdate(BookCreate):
    pass

class BookInDBBase(BaseModel):
    id: int
    name: str
    author_id: int

    class Config:
        orm_mode = True


class Book(BookInDBBase):
    pass