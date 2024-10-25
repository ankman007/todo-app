from typing import List
from loguru import logger
from pydantic import BaseModel
from psycopg2 import DatabaseError
from app.database import get_db_connection
from psycopg2.extras import RealDictCursor

class ToDo(BaseModel):
    todo_id: int
    title: str
    complete: bool = False 
    
    @classmethod
    def add_todo(cls, title: str, complete: bool):
        """Add a new todo item to the database, or update if it already exists."""
        try:
            with get_db_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute('''
                        INSERT INTO todo_db (title, completed)
                        VALUES (%s, %s)
                        RETURNING todo_id 
                    ''', (title, complete))

                    result = cursor.fetchone()
                    todo_id = result[0] if result else None
                    conn.commit()
                    return todo_id

        except DatabaseError as e:
            logger.error(f"Error adding todo item: {e}")
            conn.rollback()  
            return None
    
    @classmethod
    def update_todo(cls, todo_id: int, title: str, complete: bool):
        """Update the todo item in the database."""
        try:
            with get_db_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(''' 
                    INSERT INTO todo_db (title, completed)
                    VALUES (%s, %s)
                    ON CONFLICT (title)
                    DO UPDATE SET completed = EXCLUDED.completed
                    RETURNING todo_id;
                    ''', (title, complete))

                    conn.commit()
                    logger.info(f"Todo item {todo_id} updated successfully.")
        except DatabaseError as e:
            logger.error(f"Error updating todo item {todo_id}: {e}")
            conn.rollback()  

    @classmethod
    def delete_todo(cls, todo_id: int):
        """Delete the todo item from the database."""
        try:
            with get_db_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(''' 
                        DELETE FROM todo_db 
                        WHERE todo_id = %s
                    ''', (todo_id,))
                    
                    conn.commit()
                    logger.info(f"Todo item {todo_id} deleted successfully.")
        except DatabaseError as e:
            logger.error(f"Error deleting todo item {todo_id}: {e}")

    @classmethod
    def get_todo(cls, todo_id: int):
        """Fetch a todo item from the database by id."""
        try:
            with get_db_connection() as conn:
                with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                    cursor.execute(''' 
                        SELECT * FROM todo_db
                        WHERE todo_id = %s
                    ''', (todo_id,))
                    
                    todo = cursor.fetchone()
                    if todo:
                        logger.info(f"Todo item {todo_id} fetched successfully.")
                        return cls(todo_id=todo['todo_id'], title=todo['title'], complete=todo['completed'])
                    else:
                        logger.warning(f"Todo item {todo_id} not found.")
                        return None
        except DatabaseError as e:
            logger.error(f"Error fetching todo item {todo_id}: {e}")
            return None

    @classmethod
    def get_todos(cls):
        """Fetch all todo items from the database"""
        try: 
            with get_db_connection() as conn:
                with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                    cursor.execute(''' 
                    SELECT * FROM todo_db
                    ''')
                    todos = cursor.fetchall()
                    return todos
        except DatabaseError as e:
            logger.error(f"Error fetching todo items: {e}")
            return []

    @classmethod
    def add_todo(cls, title: str, complete: bool) -> int:
        """Add a new todo item to the database, or update if it already exists."""
        try:
            with get_db_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(''' 
                        INSERT INTO todo_db (title, completed)
                        VALUES (%s, %s)
                        ON CONFLICT (title)
                        DO UPDATE SET completed = EXCLUDED.completed
                        RETURNING todo_id;
                    ''', (title, complete))

                    todo_id = cursor.fetchone()[0]
                    conn.commit()
                    return todo_id
        except DatabaseError as e:
            logger.error(f"Error adding or updating todo item: {e}")
            print(f"DatabaseError: {e}")  
            return -1
