import os 
import psycopg2
from loguru import logger
from psycopg2.extras import RealDictCursor

def get_db_connection():
    try: 
        conn = psycopg2.connect(
            host=os.getenv("DB_HOST"),
            database=os.getenv("DB_NAME"),
            username=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
        )
        logger.info("Database connection established successfully.")
        return conn

    except psycopg2.OperationalError as e:
        logger.error(f"Failed to connect to database: {e}")
        raise