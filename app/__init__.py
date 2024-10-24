from fastapi import FastAPI

def create_app():
    app = FastAPI()
    from app.views import router as todo_router
    app.include_router(todo_router, prefix='')
    return app 