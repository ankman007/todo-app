import os 
import psycopg2
from loguru import logger
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv
from pathlib import Path

env_path = Path(__file__).resolve().parent.parent / '.env'
load_dotenv(dotenv_path=env_path)

def get_db_connection():
    try: 
        conn = psycopg2.connect(
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            host=os.getenv("DB_HOST"),  
            port=os.getenv("PORT"),
        )
        logger.info("Database connection established successfully.")
        return conn

    except psycopg2.OperationalError as e:
        logger.error(f"Failed to connect to database: {e}")
        raise

def create_table(conn):
    cursor = conn.cursor()
    create_table_query = """
    CREATE TABLE IF NOT EXISTS todo_db
    todo_id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    completed BOOLEAN NOT NULL DEFAULT FALSE,
    """
    try: 
        cursor.execute(create_table_query)
        conn.commit()
        logger.info("Table 'todo_db' created successfully.")
    except Exception as e:
        logger.error(f"Error creating table: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()
        