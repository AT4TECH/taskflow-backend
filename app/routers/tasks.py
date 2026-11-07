from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from app import crud
from app.database import get_db
from app.schemas import TaskCreate, TaskRead, TaskUpdate

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.post("", response_model=TaskRead, status_code=status.HTTP_201_CREATED)
def create_task(
    task_data: TaskCreate,
    db: Annotated[Session, Depends(get_db)],
) -> TaskRead:
    return crud.create_task(db, task_data)


@router.get("", response_model=list[TaskRead])
def read_tasks(db: Annotated[Session, Depends(get_db)]) -> list[TaskRead]:
    return crud.get_tasks(db)


@router.get("/{task_id}", response_model=TaskRead)
def read_task(
    task_id: int,
    db: Annotated[Session, Depends(get_db)],
) -> TaskRead:
    task = crud.get_task(db, task_id)
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tarea no encontrada.",
        )
    return task


@router.put("/{task_id}", response_model=TaskRead)
def replace_task(
    task_id: int,
    task_data: TaskUpdate,
    db: Annotated[Session, Depends(get_db)],
) -> TaskRead:
    task = crud.get_task(db, task_id)
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tarea no encontrada.",
        )
    return crud.update_task(db, task, task_data)


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_task(
    task_id: int,
    db: Annotated[Session, Depends(get_db)],
) -> Response:
    task = crud.get_task(db, task_id)
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tarea no encontrada.",
        )
    crud.delete_task(db, task)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
