from fastapi import FastAPI

from src.tasks.router import task_routes
from src.user.router import user_routes
from src.utils.db import Base, engine

Base.metadata.create_all(engine)


app = FastAPI(title="Task Management Application")
app.include_router(task_routes)
app.include_router(user_routes)
