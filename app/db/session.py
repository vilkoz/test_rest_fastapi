import databases
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker

from core.config import settings

engine = create_engine(settings.DB_URI, pool_pre_ping=True)
database = databases.Database(settings.DB_URI)

metadata = MetaData()