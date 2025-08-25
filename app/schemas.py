
"""
Pydantic схемы для валидации данных
"""
from typing import Optional
from pydantic import BaseModel, Field
from .models import TaskStatus


class TaskCreate(BaseModel):
    """Схема для создания задачи"""
    title: str = Field(..., min_length=1, max_length=200, description="Название задачи")
    description: Optional[str] = Field(None, max_length=1000, description="Описание задачи")
    status: Optional[TaskStatus] = Field(default=TaskStatus.CREATED, description="Статус задачи")

    class Config:
        """Конфигурация схемы"""
        json_schema_extra = {
            "example": {
                "title": "Изучить FastAPI",
                "description": "Прочитать документацию и создать тестовое приложение",
                "status": "создано"
            }
        }


class TaskUpdate(BaseModel):
    """Схема для обновления задачи"""
    title: Optional[str] = Field(None, min_length=1, max_length=200, description="Название задачи")
    description: Optional[str] = Field(None, max_length=1000, description="Описание задачи")
    status: Optional[TaskStatus] = Field(None, description="Статус задачи")

    class Config:
        """Конфигурация схемы"""
        json_schema_extra = {
            "example": {
                "title": "Изучить FastAPI (обновлено)",
                "description": "Прочитать документацию, создать тестовое приложение и написать тесты",
                "status": "в работе"
            }
        }


class TaskResponse(BaseModel):
    """Схема ответа с задачей"""
    id: str = Field(..., description="Уникальный идентификатор задачи")
    title: str = Field(..., description="Название задачи")
    description: Optional[str] = Field(None, description="Описание задачи")
    status: TaskStatus = Field(..., description="Статус задачи")

    class Config:
        """Конфигурация схемы"""
        json_schema_extra = {
            "example": {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "title": "Изучить FastAPI",
                "description": "Прочитать документацию и создать тестовое приложение",
                "status": "создано"
            }
        }


class TaskListResponse(BaseModel):
    """Схема ответа со списком задач"""
    tasks: list[TaskResponse] = Field(..., description="Список задач")
    total: int = Field(..., description="Общее количество задач")

    class Config:
        """Конфигурация схемы"""
        json_schema_extra = {
            "example": {
                "tasks": [
                    {
                        "id": "123e4567-e89b-12d3-a456-426614174000",
                        "title": "Изучить FastAPI",
                        "description": "Прочитать документацию и создать тестовое приложение",
                        "status": "создано"
                    }
                ],
                "total": 1
            }
        }

