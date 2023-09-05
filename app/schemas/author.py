from pydantic import BaseModel

class AuthorCreate(BaseModel):
    name: str

class AuthorUpdate(AuthorCreate):
    pass

class AuthorInDBBase(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True

class Author(AuthorInDBBase):
    pass
