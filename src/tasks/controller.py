from fastapi import HTTPException
from sqlalchemy.orm import Session

from src.tasks.dtos import TaskSchema
from src.tasks.models import TaskModel
from src.user.models import UserModel
from src.utils.logger import logger


def create_task(body: TaskSchema, db: Session, user: UserModel):
    logger.info("Create task request – user_id=%s", user.id)
    try:
        data = body.model_dump()
        new_task = TaskModel(title = data["title"],
                            description = data["description"],
                            is_completed = data["is_completed"],
                            user_id = user.id)
        db.add(new_task)
        db.commit()
        db.refresh(new_task)

        logger.info("Task created – id=%s, title=%s", new_task.id, new_task.title)
        return new_task

    except Exception as exc:
        logger.exception("Error creating task for user_id=%s", exc, user.id)
        db.rollback()
        raise


def get_tasks(db: Session):
    logger.debug("Fetching all tasks from DB")
    tasks = db.query(TaskModel).all()

    logger.info("Retrieved %d tasks", len(tasks))
    return tasks


def get_task_by_user(db: Session, user: UserModel):
    logger.debug("Fetching tasks for user_id=%s", user.id)
    tasks = db.query(TaskModel).filter(TaskModel.user_id == user.id).all()

    logger.info("User %s has %d tasks", user.id, len(tasks))
    return tasks


def get_one_task(task_id:int, db: Session, user=UserModel):
    logger.info("Get task request – task_id=%s, user_id=%s", task_id, user.id)
    task = db.query(TaskModel).filter(TaskModel.id == task_id).first()

    if not task:
        logger.warning("Task not found – task_id=%s", task_id)
        raise HTTPException(404, detail="Task Id is incorrect")


    if task.user_id != user.id:
        logger.warning(
            "Unauthorized task view – task_id=%s, user_id=%s", task_id, user.id
        )
        raise HTTPException(403, detail="You are not authorized to view this task")

    logger.debug("Task retrieved – id=%s, title=%s", task.id, task.title)
    return task


def update_task(body: TaskSchema, task_id: int, db: Session, user: UserModel):
    logger.info("Update task request – task_id=%s, user_id=%s", task_id, user.id)

    try:
        task = db.query(TaskModel).get(task_id)
        if not task:
            logger.warning("Task not found for update – task_id=%s", task_id)
            raise HTTPException(404, detail="Task Id is incorrect")

        # task.title = body.title
        # task.description = body.description
        # task.is_completed = body.is_completed

        if task.user_id != user.id:
            logger.warning(
                "Unauthorized update attempt – task_id=%s, user_id=%s",
                task_id,
                user.id,
            )
            raise HTTPException(403, detail="You are not authorized to update this task")

        for key, value in body.model_dump().items():
            setattr(task, key, value)

        db.add(task)
        db.commit()
        db.refresh(task)

        logger.info("Task updated – id=%s", task.id)
        return task

    except Exception as exc:
        logger.exception("Error updating task %s for user %s", task_id, user.id)
        db.rollback()
        raise


def delete_task(task_id: int, db: Session, user: UserModel):
    logger.info("Delete task request – task_id=%s, user_id=%s", task_id, user.id)
    try:
        task = db.query(TaskModel).get(task_id)

        if not task:
            logger.warning("Task not found for delete – task_id=%s", task_id)
            raise HTTPException(404, detail="Task Id is incorrect")

        if task.user_id != user.id:
            logger.warning(
                "Unauthorized delete attempt – task_id=%s, user_id=%s",
                task_id,
                user.id,
            )
            raise HTTPException(403, detail="You are not authorized to delete this task")

        db.delete(task)
        db.commit()
        logger.info("Task deleted – id=%s", task_id)


    except Exception as exc:
        logger.exception("Error deleting task %s for user %s", task_id, user.id)
        db.rollback()
        raise


def delete_all_task(db: Session):
    logger.warning("Deleting all tasks – admin action")
    try:
        db.query(TaskModel).delete()
        db.commit()
        logger.info("All tasks removed successfully")
        
    except Exception as exc:
        logger.exception("Failed to delete all tasks")
        db.rollback()
        raise

    