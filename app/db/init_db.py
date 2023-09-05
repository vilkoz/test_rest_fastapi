import logging

import models
from db.session import engine, metadata

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def init_db_tables():
    logger.info("Creating tables")
    metadata.create_all(engine)
    logger.info("DB tables created")