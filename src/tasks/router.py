from fastapi import FastAPI, APIRouter, Depends
from src.tasks import controller
from src.tasks.dtos import TaskSchema
from src.utils.db import get_db


task_routes = APIRouter(prefix="/tasks")


@task_routes.post("/create")
def create_task(body:TaskSchema, db=Depends(get_db)):
    return controller.create_task(body, db)

