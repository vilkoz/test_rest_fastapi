from typing import List, Any

from fastapi import APIRouter, HTTPException, status

from db.session import database

from models import authors
from schemas import Author, AuthorCreate, AuthorUpdate


router = APIRouter()


@router.get("/", response_model=List[Author])
async def get_authors():
    query = authors.select()
    return await database.fetch_all(query)


@router.get("/{author_id}", response_model=Author)
async def get_author_by_id(author_id: int):
    query = authors.select().where(authors.c.id == author_id)
    response = await database.fetch_one(query)
    if response is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return response


@router.post("/", response_model=Author)
async def create_author(author_in: AuthorCreate):
    query = authors.insert()
    created_id = await database.execute(query=query, values=author_in.dict())
    if created_id is None:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return Author(id=created_id, **author_in)


@router.post("/{author_id}", response_model=Author)
async def update_author(author_id: int, author_in: AuthorUpdate):
    query = authors.select().where(authors.c.id == author_id)
    response = await database.fetch_one(query)
    if response is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    query = authors.update().where(authors.c.id == author_id).values(**author_in.dict())
    response = await database.execute(query)
    query = authors.select().where(authors.c.id == author_id)
    response = await database.fetch_one(query)
    return response

@router.delete("/{author_id}", response_model=None)
async def delete_author_by_id(author_id: int):
    query = authors.delete().where(authors.c.id == author_id)
    response = await database.execute(query)
    if response == False:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return {"status": "success"}