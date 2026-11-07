from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Task
from app.schemas import TaskCreate, TaskUpdate


def get_tasks(db: Session) -> list[Task]:
    return list(db.scalars(select(Task).order_by(Task.id)))


def get_task(db: Session, task_id: int) -> Task | None:
    return db.get(Task, task_id)


def create_task(db: Session, task_data: TaskCreate) -> Task:
    task = Task(
        title=task_data.title,
        description=task_data.description,
        priority=task_data.priority.value,
        status=task_data.status.value,
    )
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


def update_task(
    db: Session,
    task: Task,
    task_data: TaskUpdate,
) -> Task:
    task.title = task_data.title
    task.description = task_data.description
    task.priority = task_data.priority.value
    task.status = task_data.status.value
    db.commit()
    db.refresh(task)
    return task


def delete_task(db: Session, task: Task) -> None:
    db.delete(task)
    db.commit()
