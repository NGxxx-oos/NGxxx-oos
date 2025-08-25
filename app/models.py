
"""
Модели данных для Task Management API
"""
import uuid
from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field


class TaskStatus(str, Enum):
    """Статусы задач"""
    CREATED = "создано"
    IN_PROGRESS = "в работе"
    COMPLETED = "завершено"


class Task(BaseModel):
    """Модель задачи"""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), description="Уникальный идентификатор задачи")
    title: str = Field(..., min_length=1, max_length=200, description="Название задачи")
    description: Optional[str] = Field(None, max_length=1000, description="Описание задачи")
    status: TaskStatus = Field(default=TaskStatus.CREATED, description="Статус задачи")

    class Config:
        """Конфигурация модели"""
        json_schema_extra = {
            "example": {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "title": "Изучить FastAPI",
                "description": "Прочитать документацию и создать тестовое приложение",
                "status": "создано"
            }
        }

