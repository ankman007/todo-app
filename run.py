from psycopg2.extras import execute_batch
from app.database import get_db_connection
from psycopg2 import DatabaseError
from loguru import logger

# Create table query
create_table_query = """
CREATE TABLE IF NOT EXISTS todo_db (
    todo_id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    completed BOOLEAN NOT NULL DEFAULT FALSE
);
"""

# Insert query
insert_query = """
INSERT INTO todo_db (title, completed)
VALUES (%s, %s)
"""

todos = [
    ('Wash Laptop', False),
    ('Take fish home', True),
    ('Fill bottles', False),
]

conn = None  
cursor = None  

try: 
    conn = get_db_connection()
    cursor = conn.cursor()

    # Create the table
    cursor.execute(create_table_query)

    # Insert multiple rows
    execute_batch(cursor, insert_query, todos)
    conn.commit()
    logger.info("Multiple rows inserted successfully.")

except DatabaseError as e:
    if conn: 
        conn.rollback()  
    logger.error(f"Error inserting multiple todo items: {e}")

finally: 
    if cursor: 
        cursor.close()  
    if conn: 
        conn.close()  

logger.info("Hello world")
