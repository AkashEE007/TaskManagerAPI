from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from src.tasks import controller
from src.tasks.dtos import TaskResponseSchema, TaskSchema, DeleteTaskConfirmation
from src.user.models import UserModel
from src.utils.db import get_db
from src.utils.helpers import is_authenticated, require_admin

task_routes = APIRouter(prefix="/tasks", tags=["Tasks"])


@task_routes.post("/create_task", response_model=TaskResponseSchema, status_code=status.HTTP_201_CREATED)
def create_task(body:TaskSchema, db: Session=Depends(get_db), user: UserModel=Depends(is_authenticated)):
    return controller.create_task(body, db, user)


@task_routes.get("/get_all_tasks", response_model=list[TaskResponseSchema], status_code=status.HTTP_200_OK)
def get_all_tasks(skip: int=0, limit: int=20, db: Session=Depends(get_db), user: UserModel=Depends(require_admin)):
    return controller.get_tasks(db, skip=skip, limit=limit)


@task_routes.get("/get_user_tasks", response_model=list[TaskResponseSchema], status_code=status.HTTP_200_OK)
def get_user_tasks(skip: int=0, limit: int=20, db: Session=Depends(get_db), user: UserModel=Depends(is_authenticated)):
    return controller.get_task_by_user(db, user, skip=skip, limit=limit)


@task_routes.get("/get_one_task/{task_id}", response_model=TaskResponseSchema, status_code=status.HTTP_200_OK)
def get_one_task(task_id: int, db: Session=Depends(get_db), user: UserModel=Depends(is_authenticated)):
    return controller.get_one_task(task_id, db, user)


@task_routes.put("/update_task/{task_id}", response_model=TaskResponseSchema, status_code=status.HTTP_200_OK)
def update_task(body: TaskSchema, task_id: int, db: Session=Depends(get_db), user: UserModel=Depends(is_authenticated)):
    return controller.update_task(body, task_id, db, user)


@task_routes.delete("/delete_task/{task_id}", response_model=None, status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int, db: Session=Depends(get_db), user: UserModel=Depends(is_authenticated)):
    return controller.delete_task(task_id, db, user)


@task_routes.post("/admin/tasks/delete-all", status_code=status.HTTP_204_NO_CONTENT)
def delete_all_tasks(body: DeleteTaskConfirmation, db: Session=Depends(get_db), user: UserModel=Depends(require_admin)):
    return controller.delete_all_task(db, body)

