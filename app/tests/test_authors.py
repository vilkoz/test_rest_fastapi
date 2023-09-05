from fastapi.testclient import TestClient
import pytest
from sqlalchemy import create_engine
from sqlalchemy_utils.functions import database_exists, create_database, drop_database

from app.core.config import settings, AppEnvironments

settings.APP_ENVIRONMENT = AppEnvironments.test

from app.main import app
from app.db.init_db import init_db_tables
import crud
from app.schemas import AuthorCreate

client = TestClient(app)


def db_preparation():
    dsn = settings.TEST_DB_URI
    engine = create_engine(dsn)
    if database_exists(engine.url):
        drop_database(engine.url)
    create_database(engine.url)
    conn = engine.connect()
    conn.close()


@pytest.fixture(autouse=True)
def init_db():
    db_preparation()
    init_db_tables()


@pytest.mark.asyncio
async def test_get_authors():
    res = client.get("/api/v1/authors")
    assert res.status_code == 200
    assert res.json() == []
    await crud.author.create(obj_in=AuthorCreate(name="author1"))
    await crud.author.create(obj_in=AuthorCreate(name="author2"))
    res = client.get("/api/v1/authors")
    assert res.status_code == 200
    assert res.json() == [
        {
            "id": 1,
            "name": "author1",
        },
        {
            "id": 2,
            "name": "author2",
        },
    ]


@pytest.mark.asyncio
async def test_get_author_by_id():
    res = client.get("/api/v1/authors/2")
    assert res.status_code == 404
    await crud.author.create(obj_in=AuthorCreate(name="author1"))
    await crud.author.create(obj_in=AuthorCreate(name="author2"))
    res = client.get("/api/v1/authors/2")
    assert res.status_code == 200
    assert res.json() == {"id": 2, "name": "author2"}


@pytest.mark.asyncio
async def test_create_author():
    res = client.post("/api/v1/authors", json={"name": "test_author"})
    assert res.status_code == 200
    assert res.json() == {"id": 1, "name": "test_author"}
    author = await crud.author.get(1)
    assert author.id == 1
    assert author.name == "test_author"


@pytest.mark.asyncio
async def test_update_author():
    res = client.patch("/api/v1/authors/1", json={"name": "test_author"})
    assert res.status_code == 404
    await crud.author.create(obj_in=AuthorCreate(name="author1"))
    await crud.author.create(obj_in=AuthorCreate(name="author2"))
    res = client.patch("/api/v1/authors/1", json={"name": "test_author"})
    assert res.status_code == 200
    assert res.json() == {"id": 1, "name": "test_author"}
    author = await crud.author.get(1)
    assert author.id == 1
    assert author.name == "test_author"


@pytest.mark.asyncio
async def test_delete_author():
    res = client.delete("/api/v1/authors/1")
    assert res.status_code == 404
    await crud.author.create(obj_in=AuthorCreate(name="author1"))
    await crud.author.create(obj_in=AuthorCreate(name="author2"))
    res = client.delete("/api/v1/authors/1")
    assert res.status_code == 200
    assert res.json() == {"status": "success"}
    author = await crud.author.get(1)
    assert author is None
