import databases
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker

from core.config import settings, AppEnvironments

db_uri = settings.DB_URI
if settings.APP_ENVIRONMENT == AppEnvironments.test:
    db_uri = settings.TEST_DB_URI

engine = create_engine(db_uri, pool_pre_ping=True)
database = databases.Database(db_uri)

metadata = MetaData()