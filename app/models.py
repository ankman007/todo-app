from typing import List
from loguru import logger
from pydantic import BaseModel
from psycopg2 import DatabaseError
from app.database import get_db_connection
from psycopg2.extras import RealDictCursor
from app.schemas import TodoItemResponse, TodoListResponse

class ToDo(BaseModel):
    todo_id: int
    title: str
    complete: bool = False 

    def update_todo(self, todo_id: int, title:str, complete: bool):
        """Update the todo item in the database."""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE todo_db1
                SET title = %s, completed = %s 
                WHERE todo_id = %s
            ''', (title, complete, todo_id))

            conn.commit()
            logger.info(f"Todo item {todo_id} updated successfully.")
        except DatabaseError as e:
            logger.error(f"Error updating todo item {todo_id}: {e}")
            conn.rollback()  
        finally:
            cursor.close()
            conn.close()   

    def delete_todo(self, todo_id: int):
        """Delete the todo item from the database."""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute('''
                DELETE FROM todo_db1
                WHERE todo_id = %s
            ''', (todo_id,))

            conn.commit()
            logger.info(f"Todo item {todo_id} deleted successfully.")
        except DatabaseError as e:
            logger.error(f"Error deleting todo item {todo_id}: {e}")
            conn.rollback()  
        finally:
            cursor.close()
            conn.close()
    
    @classmethod
    def get_todo(cls, todo_id: int) -> TodoItemResponse:
        """Fetch a todo item from the database by id."""
        try:
            conn = get_db_connection()
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            cursor.execute('''
                SELECT * FROM todo_db1
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
        
        finally:
            cursor.close()
            conn.close()
            
    @classmethod
    def get_all_todo(cls) -> TodoListResponse:
        """Fetch all todo items from the database"""
        try: 
            conn = get_db_connection()
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            cursor.execute('''
            SELECT * FROM todo_db1
            ''')
            todos = cursor.fetchall()
            todo_items = [TodoItemResponse(**todo) for todo in todos]
            return todo_items
        
        except DatabaseError as e:
            logger.error(f"Error fetching todo items: {e}")
            conn.rollback()
            return []

        finally:
            cursor.close()
            conn.close()
            
    @staticmethod
    def add_todo(title: str, complete: bool) -> int:
        """Add a new todo item to the database."""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO todo_db1 (title, completed)
                VALUES (%s, %s) RETURNING todo_id;
            ''', (title, complete))

            todo_id = cursor.fetchone()[0]
            conn.commit()
            return todo_id

        except DatabaseError as e:
            logger.error(f"Error adding todo item: {e}")
            conn.rollback()

        finally:
            cursor.close()
            conn.close()