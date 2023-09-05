from typing import List, Any

from fastapi import APIRouter, HTTPException, status

from db.session import database

from models import authors
from schemas import Author, AuthorCreate, AuthorUpdate
import crud


router = APIRouter()


@router.get("/", response_model=List[Author])
async def get_authors():
    return await crud.author.get_all()


@router.get("/{author_id}", response_model=Author)
async def get_author_by_id(author_id: int):
    return await crud.author.get_or_404(id=author_id)


@router.post("/", response_model=Author)
async def create_author(author_in: AuthorCreate):
    return await crud.author.create(obj_in=author_in)


@router.post("/{author_id}", response_model=Author)
async def update_author(author_id: int, author_in: AuthorUpdate):
    return await crud.author.update(id=author_id, obj_in=author_in)


@router.delete("/{author_id}", response_model=None)
async def delete_author_by_id(author_id: int):
    await crud.author.remove(id=author_id)
    return {"status": "success"}
