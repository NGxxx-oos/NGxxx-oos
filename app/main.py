
"""
Основное FastAPI приложение для управления задачами
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .models import Task

# Создание экземпляра FastAPI приложения
app = FastAPI(
    title="Task Management API",
    description="REST API для управления задачами с CRUD операциями",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Настройка CORS для разрешения запросов с любых источников
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory хранилище задач (в реальном приложении использовалась бы база данных)
tasks_storage: dict[str, Task] = {}


@app.get("/")
async def root():
    """Корневой endpoint для проверки работы API"""
    return {
        "message": "Task Management API",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc"
    }


@app.get("/health")
async def health_check():
    """Endpoint для проверки состояния сервиса"""
    return {
        "status": "healthy",
        "tasks_count": len(tasks_storage)
    }



# Импорты для API endpoints
from typing import Optional
from fastapi import HTTPException, Query
from .schemas import TaskCreate, TaskUpdate, TaskResponse, TaskListResponse
from .models import TaskStatus
from .crud import TaskCRUD

# Инициализация CRUD операций
task_crud = TaskCRUD(tasks_storage)


@app.post("/tasks", response_model=TaskResponse, status_code=201)
async def create_task(task_data: TaskCreate):
    """Создание новой задачи"""
    task = task_crud.create_task(task_data)
    return TaskResponse(
        id=task.id,
        title=task.title,
        description=task.description,
        status=task.status
    )


@app.get("/tasks/{task_id}", response_model=TaskResponse)
async def get_task(task_id: str):
    """Получение задачи по ID"""
    task = task_crud.get_task(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Задача не найдена")
    
    return TaskResponse(
        id=task.id,
        title=task.title,
        description=task.description,
        status=task.status
    )


@app.get("/tasks", response_model=TaskListResponse)
async def get_tasks(status: Optional[TaskStatus] = Query(None, description="Фильтр по статусу задачи")):
    """Получение списка всех задач с возможностью фильтрации по статусу"""
    tasks = task_crud.get_tasks(status)
    task_responses = [
        TaskResponse(
            id=task.id,
            title=task.title,
            description=task.description,
            status=task.status
        )
        for task in tasks
    ]
    
    return TaskListResponse(
        tasks=task_responses,
        total=len(task_responses)
    )


@app.put("/tasks/{task_id}", response_model=TaskResponse)
async def update_task(task_id: str, task_data: TaskUpdate):
    """Обновление существующей задачи"""
    task = task_crud.update_task(task_id, task_data)
    if not task:
        raise HTTPException(status_code=404, detail="Задача не найдена")
    
    return TaskResponse(
        id=task.id,
        title=task.title,
        description=task.description,
        status=task.status
    )


@app.delete("/tasks/{task_id}", status_code=204)
async def delete_task(task_id: str):
    """Удаление задачи по ID"""
    success = task_crud.delete_task(task_id)
    if not success:
        raise HTTPException(status_code=404, detail="Задача не найдена")
    
    return None

