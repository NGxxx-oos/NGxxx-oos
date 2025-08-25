
"""
CRUD операции для работы с задачами
"""
from typing import Optional, List
from .models import Task, TaskStatus
from .schemas import TaskCreate, TaskUpdate


class TaskCRUD:
    """Класс для выполнения CRUD операций с задачами"""
    
    def __init__(self, storage: dict[str, Task]):
        """Инициализация с хранилищем данных"""
        self.storage = storage
    
    def create_task(self, task_data: TaskCreate) -> Task:
        """Создание новой задачи"""
        task = Task(
            title=task_data.title,
            description=task_data.description,
            status=task_data.status or TaskStatus.CREATED
        )
        self.storage[task.id] = task
        return task
    
    def get_task(self, task_id: str) -> Optional[Task]:
        """Получение задачи по ID"""
        return self.storage.get(task_id)
    
    def get_tasks(self, status: Optional[TaskStatus] = None) -> List[Task]:
        """Получение списка всех задач с возможностью фильтрации по статусу"""
        tasks = list(self.storage.values())
        if status:
            tasks = [task for task in tasks if task.status == status]
        return tasks
    
    def update_task(self, task_id: str, task_data: TaskUpdate) -> Optional[Task]:
        """Обновление существующей задачи"""
        task = self.storage.get(task_id)
        if not task:
            return None
        
        # Обновляем только переданные поля
        update_data = task_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(task, field, value)
        
        self.storage[task_id] = task
        return task
    
    def delete_task(self, task_id: str) -> bool:
        """Удаление задачи по ID"""
        if task_id in self.storage:
            del self.storage[task_id]
            return True
        return False
    
    def get_tasks_count(self) -> int:
        """Получение общего количества задач"""
        return len(self.storage)

