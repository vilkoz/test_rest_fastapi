from typing import List, Optional

from fastapi import APIRouter, HTTPException, status

from db.session import database

from models import books
from schemas import Book, BookCreate, BookUpdate
import crud


router = APIRouter()


@router.get("/", response_model=List[Book])
async def get_books(*, author_id: Optional[int] = None):
    filter = None
    if author_id is not None:
        filter = books.c.author_id == author_id
    return await crud.book.get_all(filter=filter)


@router.get("/{book_id}", response_model=Book)
async def get_book_by_id(book_id: int):
    return await crud.book.get_or_404(id=book_id)


@router.post("/", response_model=Book)
async def create_book(book_in: BookCreate):
    await crud.author.get_or_404(id=book_in.author_id)
    return await crud.book.create(obj_in=book_in)


@router.patch("/{book_id}", response_model=Book)
async def update_book(book_id: int, book_in: BookUpdate):
    await crud.author.get_or_404(id=book_in.author_id)
    return await crud.book.update(id=book_id, obj_in=book_in)


@router.delete("/{book_id}", response_model=None)
async def delete_book_by_id(book_id: int):
    await crud.book.remove(id=book_id)
    return {"status": "success"}
