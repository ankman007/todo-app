from pydantic import BaseModel
from typing import List, Optional

class TodoCreate(BaseModel):
    title: str
    complete: Optional[bool] = False

class TodoItemResponse(BaseModel):
    todo_id: int 
    title: str
    complete: bool 

class TodoListResponse(BaseModel):
    todos: List[TodoItemResponse]