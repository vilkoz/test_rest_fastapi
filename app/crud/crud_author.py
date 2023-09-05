from crud.base import CRUDBase
from models import authors
from schemas import Author, AuthorCreate, AuthorUpdate

class CRUDAuthor(CRUDBase[authors, Author, AuthorCreate, AuthorUpdate]):
    pass

author = CRUDAuthor(authors)