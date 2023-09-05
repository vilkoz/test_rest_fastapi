import sqlalchemy
from db.session import metadata

authors = sqlalchemy.Table(
    "author",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("name", sqlalchemy.String, nullable=False)
)

books = sqlalchemy.Table(
    "book",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("name", sqlalchemy.String, nullable=False),
    sqlalchemy.Column("author_id", sqlalchemy.ForeignKey("author.id")),
)