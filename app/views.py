from loguru import logger
import traceback
from app.models import ToDo 
from app.database import get_db_connection, create_table
from fastapi import APIRouter, HTTPException
from app.schemas import TodoCreate, TodoItemResponse, TodoListResponse

router = APIRouter()

@router.get('/')
def index():
    try:
        conn = get_db_connection()
        detail = "Database connection made successfully." if conn else "Encountered error when connecting to database."
        create_table(conn)
        return {"message": detail}
    except Exception as e:
        logger.error(f"Error occurred: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get('/get_todos')
def get_todos():
    print(type(ToDo.get_todos()))
    return ToDo.get_todos()

@router.get('/get_todo/{todo_id}')
def get_todo(todo_id: int) -> TodoItemResponse:
    todo = ToDo.get_todo(todo_id=todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="ToDo not found")
    return todo

@router.put('/update_todo/{todo_id}')
def update_todo(todo_id: int, updated_todo: TodoCreate):
    if not ToDo.get_todo(todo_id):
        raise HTTPException(status_code=404, detail="ToDo not found")
    ToDo.update_todo(todo_id=todo_id, title=updated_todo.title, complete=updated_todo.complete)
    return {**updated_todo.dict(), "todo_id": todo_id}
    
@router.delete('/delete_todo/{todo_id}')
def delete_todo(todo_id: int):
    ToDo.delete_todo(todo_id=todo_id)
    return {"detail": "ToDo deleted"}

@router.post("/add_todo")
def add_todo(todo: TodoCreate):
    todo_id = ToDo.add_todo(title=todo.title, complete=todo.complete)
    print(todo_id, todo)
    return {**todo.dict(), "todo_id": todo_id}
    