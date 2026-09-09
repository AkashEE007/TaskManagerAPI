from src.tasks.dtos import TaskSchema
from sqlalchemy.orm import Session
from src.tasks.models import TaskModel
from fastapi import HTTPException, status
from src.user.models import UserModel

def create_task(body: TaskSchema, db: Session, user: UserModel):
    data = body.model_dump()
    new_task = TaskModel(title = data["title"],
                         description = data["description"],
                         is_completed = data["is_completed"],
                         user_id = user.id)
    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    return new_task


def get_tasks(db: Session):
    tasks = db.query(TaskModel).all()
    return tasks


def get_task_by_user(db: Session, user: UserModel):
    tasks = db.query(TaskModel).filter(TaskModel.user_id == user.id).all()
    return tasks


def get_one_task(task_id:int, db: Session):
    task = db.query(TaskModel).get(task_id)
    if not task:
        raise HTTPException(404, detail="Task Id is incorrect")

    return task


def update_task(body: TaskSchema, task_id: int, db: Session):
    task = db.query(TaskModel).get(task_id)
    if not task:
        raise HTTPException(404, detail="Task Id is incorrect")

    # task.title = body.title
    # task.description = body.description
    # task.is_completed = body.is_completed

    for key, value in body.model_dump().items():
        setattr(task, key, value)

    db.add(task)
    db.commit()
    db.refresh(task)

    return task


def delete_task(task_id: int, db: Session):
    task = db.query(TaskModel).get(task_id)

    if not task:
        raise HTTPException(404, detail="Task Id is incorrect")

    db.delete(task)
    db.commit()

    return None


def delete_all_task(db: Session):
    db.query(TaskModel).delete()
    db.commit()