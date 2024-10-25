from psycopg2.extras import execute_batch
from app.database import get_db_connection
from psycopg2 import DatabaseError
from loguru import logger

create_table_query = """
CREATE TABLE IF NOT EXISTS todo_db (
    todo_id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    completed BOOLEAN NOT NULL DEFAULT FALSE
);
"""

insert_query = """
INSERT INTO todo_db (title, completed)
VALUES (%s, %s)
ON CONFLICT (title)
DO UPDATE SET completed = EXCLUDED.completed;
"""

todos = [
    ('Wash Laptop', False),
    ('Take fish home', True),
    ('Fill bottles', False),
]

try: 
    with get_db_connection() as conn:
        with conn.cursor() as cursor: 
            cursor.execute(create_table_query)
            execute_batch(cursor, insert_query, todos)
            conn.commit()
            logger.info("Multiple rows inserted successfully.")

except DatabaseError as e:
    logger.error(f"Error inserting multiple todo items: {e}")