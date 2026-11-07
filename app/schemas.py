from enum import Enum

from pydantic import BaseModel, ConfigDict, field_validator


class TaskStatus(str, Enum):
    PENDIENTE = "pendiente"
    EN_PROGRESO = "en_progreso"
    COMPLETADA = "completada"


class TaskPriority(str, Enum):
    BAJA = "baja"
    MEDIA = "media"
    ALTA = "alta"


class TaskFields(BaseModel):
    title: str
    priority: TaskPriority
    status: TaskStatus
    description: str | None = None

    @field_validator("title")
    @classmethod
    def validate_title(cls, value: str) -> str:
        title = value.strip()
        if not title:
            raise ValueError("El título no puede estar vacío.")
        return title


class TaskCreate(TaskFields):
    pass


class TaskUpdate(TaskFields):
    pass


class TaskRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    description: str | None
    priority: TaskPriority
    status: TaskStatus
