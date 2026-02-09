from sqlalchemy import create_engine
from utils.logger import get_logger

logger = get_logger(__name__)

def connect_db(db_url):
    try:
        engine = create_engine(db_url)
        with engine.connect() as conn:
            pass
        print("✅ Connected to PostgreSQL successfully!")
        logger.info("Connected to PostgreSQL successfully")
        return engine
    except Exception as e:
        print("❌ Connection failed")
        logger.error("Database connection failed", exc_info=True)
        raise
