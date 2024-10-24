from loguru import logger
import traceback
from app.models import ToDo 
from app.database import get_db_connection, create_table
from fastapi import APIRouter, HTTPException
from app.schemas import TodoCreate, TodoItemResponse, TodoListResponse

router = APIRouter()

@router.get('/')
def index() -> str:
    try:
        conn = get_db_connection()
        detail = "Database connection made successfully." if conn else "Encountered error when connecting to database."
        create_table(conn)
        return {"message": detail}
    except Exception as e:
        logger.error(f"Error occurred in index: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get('/get_todos')
def get_todos():
    try:
        todos = ToDo.get_todos()
        return todos
    except Exception as e:
        logger.error(f"Error occurred while fetching todos: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get('/get_todo/{todo_id}', response_model=TodoItemResponse)
def get_todo(todo_id: int) -> TodoItemResponse:
    try:
        todo = ToDo.get_todo(todo_id=todo_id)
        if not todo:
            raise HTTPException(status_code=404, detail="ToDo not found")
        return todo
    except Exception as e:
        logger.error(f"Error occurred while fetching todo {todo_id}: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.put('/update_todo/{todo_id}')
def update_todo(todo_id: int, updated_todo: TodoCreate):
    try:
        if not ToDo.get_todo(todo_id):
            raise HTTPException(status_code=404, detail="ToDo not found")
        ToDo.update_todo(todo_id=todo_id, title=updated_todo.title, complete=updated_todo.complete)
        return {**updated_todo.dict(), "todo_id": todo_id}
    except Exception as e:
        logger.error(f"Error occurred while updating todo {todo_id}: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.delete('/delete_todo/{todo_id}')
def delete_todo(todo_id: int):
    try:
        ToDo.delete_todo(todo_id=todo_id)
        return {"detail": "ToDo deleted"}
    except Exception as e:
        logger.error(f"Error occurred while deleting todo {todo_id}: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.post("/add_todo")
def add_todo(todo: TodoCreate):
    try:
        todo_id = ToDo.add_todo(title=todo.title, complete=todo.complete)
        return {**todo.dict(), "todo_id": todo_id}  
    except Exception as e:
        logger.error(f"Error occurred while adding todo: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail="Internal server error")
