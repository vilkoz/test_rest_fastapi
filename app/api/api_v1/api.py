from fastapi import APIRouter

from api.api_v1.endpoints import authors, books

api_router = APIRouter()
api_router.include_router(authors.router, prefix="/authors")
api_router.include_router(books.router, prefix="/books")