from crud.base import CRUDBase
from models import books
from schemas import Book, BookCreate, BookUpdate


class CRUDBook(CRUDBase[books, Book, BookCreate, BookUpdate]):
    pass


book = CRUDBook(books)
