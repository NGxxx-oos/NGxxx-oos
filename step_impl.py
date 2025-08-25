"""
Step implementations для тестирования Task Management API
"""
import json
import time
import subprocess
import requests
from getgauge.python import step, before_scenario, after_scenario

# Глобальные переменные для хранения состояния тестов
api_process = None
base_url = "http://localhost:8000"
created_tasks = []
last_response = None
last_task_id = None


@before_scenario
def setup_scenario():
    """Настройка перед каждым сценарием"""
    global created_tasks, last_response, last_task_id
    created_tasks = []
    last_response = None
    last_task_id = None


@after_scenario
def cleanup_scenario():
    """Очистка после каждого сценария"""
    global api_process
    if api_process:
        api_process.terminate()
        api_process.wait()
        api_process = None
    time.sleep(1)  # Дать время серверу завершиться


@step("Запустить API сервер")
def start_api_server():
    """Запуск API сервера"""
    global api_process
    if api_process is None:
        api_process = subprocess.Popen(
            ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"],
            cwd="/home/ubuntu/task_management_api"
        )
        time.sleep(3)  # Дать время серверу запуститься


@step("Создать новую задачу с названием <title> и описанием <description>")
def create_task(title, description):
    """Создание новой задачи"""
    global last_response, last_task_id, created_tasks
    
    task_data = {
        "title": title,
        "description": description,
        "status": "создано"
    }
    
    last_response = requests.post(f"{base_url}/tasks", json=task_data)
    
    if last_response.status_code == 201:
        task = last_response.json()
        last_task_id = task["id"]
        created_tasks.append(task)


@step("Проверить, что задача создана успешно")
def verify_task_created():
    """Проверка успешного создания задачи"""
    assert last_response.status_code == 201, f"Ожидался код 201, получен {last_response.status_code}"
    task = last_response.json()
    assert "id" in task, "Ответ должен содержать ID задачи"
    assert task["title"], "Задача должна иметь название"


@step("Проверить, что задача имеет статус <status>")
def verify_task_status(status):
    """Проверка статуса задачи"""
    task = last_response.json()
    assert task["status"] == status, f"Ожидался статус '{status}', получен '{task['status']}'"


@step("Получить список всех задач")
def get_all_tasks():
    """Получение списка всех задач"""
    global last_response
    last_response = requests.get(f"{base_url}/tasks")


@step("Проверить, что в списке есть обе задачи")
def verify_both_tasks_in_list():
    """Проверка наличия обеих задач в списке"""
    assert last_response.status_code == 200, f"Ожидался код 200, получен {last_response.status_code}"
    response_data = last_response.json()
    assert response_data["total"] >= 2, f"Ожидалось минимум 2 задачи, получено {response_data['total']}"


@step("Получить задачу по её ID")
def get_task_by_id():
    """Получение задачи по ID"""
    global last_response
    assert last_task_id, "ID задачи не установлен"
    last_response = requests.get(f"{base_url}/tasks/{last_task_id}")


@step("Проверить, что полученная задача соответствует созданной")
def verify_task_matches():
    """Проверка соответствия полученной задачи созданной"""
    assert last_response.status_code == 200, f"Ожидался код 200, получен {last_response.status_code}"
    task = last_response.json()
    assert task["id"] == last_task_id, "ID задачи не совпадает"


@step("Обновить задачу, изменив статус на <status>")
def update_task_status(status):
    """Обновление статуса задачи"""
    global last_response
    assert last_task_id, "ID задачи не установлен"
    
    update_data = {"status": status}
    last_response = requests.put(f"{base_url}/tasks/{last_task_id}", json=update_data)


@step("Проверить, что задача обновлена успешно")
def verify_task_updated():
    """Проверка успешного обновления задачи"""
    assert last_response.status_code == 200, f"Ожидался код 200, получен {last_response.status_code}"


@step("Удалить задачу по её ID")
def delete_task():
    """Удаление задачи по ID"""
    global last_response
    assert last_task_id, "ID задачи не установлен"
    last_response = requests.delete(f"{base_url}/tasks/{last_task_id}")


@step("Проверить, что задача удалена успешно")
def verify_task_deleted():
    """Проверка успешного удаления задачи"""
    assert last_response.status_code == 204, f"Ожидался код 204, получен {last_response.status_code}"


@step("Проверить, что задача больше не существует")
def verify_task_not_exists():
    """Проверка, что задача больше не существует"""
    response = requests.get(f"{base_url}/tasks/{last_task_id}")
    assert response.status_code == 404, f"Ожидался код 404, получен {response.status_code}"


@step("Обновить вторую задачу, изменив статус на <status>")
def update_second_task_status(status):
    """Обновление статуса второй задачи"""
    global last_response
    assert len(created_tasks) >= 2, "Недостаточно созданных задач"
    
    second_task_id = created_tasks[1]["id"]
    update_data = {"status": status}
    last_response = requests.put(f"{base_url}/tasks/{second_task_id}", json=update_data)


@step("Получить список задач со статусом <status>")
def get_tasks_by_status(status):
    """Получение списка задач по статусу"""
    global last_response
    last_response = requests.get(f"{base_url}/tasks", params={"status": status})


@step("Проверить, что в списке только одна задача со статусом <status>")
def verify_single_task_with_status(status):
    """Проверка наличия одной задачи с определенным статусом"""
    assert last_response.status_code == 200, f"Ожидался код 200, получен {last_response.status_code}"
    response_data = last_response.json()
    
    tasks_with_status = [task for task in response_data["tasks"] if task["status"] == status]
    assert len(tasks_with_status) == 1, f"Ожидалась 1 задача со статусом '{status}', получено {len(tasks_with_status)}"


@step("Попытаться получить задачу с несуществующим ID")
def try_get_nonexistent_task():
    """Попытка получить несуществующую задачу"""
    global last_response
    fake_id = "00000000-0000-0000-0000-000000000000"
    last_response = requests.get(f"{base_url}/tasks/{fake_id}")


@step("Проверить, что возвращается ошибка 404")
def verify_404_error():
    """Проверка ошибки 404"""
    assert last_response.status_code == 404, f"Ожидался код 404, получен {last_response.status_code}"


@step("Попытаться обновить задачу с несуществующим ID")
def try_update_nonexistent_task():
    """Попытка обновить несуществующую задачу"""
    global last_response
    fake_id = "00000000-0000-0000-0000-000000000000"
    update_data = {"status": "в работе"}
    last_response = requests.put(f"{base_url}/tasks/{fake_id}", json=update_data)


@step("Попытаться удалить задачу с несуществующим ID")
def try_delete_nonexistent_task():
    """Попытка удалить несуществующую задачу"""
    global last_response
    fake_id = "00000000-0000-0000-0000-000000000000"
    last_response = requests.delete(f"{base_url}/tasks/{fake_id}")


@step("Попытаться создать задачу с пустым названием")
def try_create_task_empty_title():
    """Попытка создать задачу с пустым названием"""
    global last_response
    task_data = {
        "title": "",
        "description": "Описание"
    }
    last_response = requests.post(f"{base_url}/tasks", json=task_data)


@step("Проверить, что возвращается ошибка валидации")
def verify_validation_error():
    """Проверка ошибки валидации"""
    assert last_response.status_code == 422, f"Ожидался код 422, получен {last_response.status_code}"


@step("Попытаться создать задачу со слишком длинным названием")
def try_create_task_long_title():
    """Попытка создать задачу со слишком длинным названием"""
    global last_response
    long_title = "a" * 201  # Превышает лимит в 200 символов
    task_data = {
        "title": long_title,
        "description": "Описание"
    }
    last_response = requests.post(f"{base_url}/tasks", json=task_data)



@step("Проверить, что статус задачи изменился на <status>")
def verify_task_status_changed(status):
    """Проверка изменения статуса задачи"""
    task = last_response.json()
    assert task["status"] == status, f"Ожидался статус '{status}', получен '{task['status']}'"


@step("Очистить все задачи")
def clear_all_tasks():
    """Очистка всех задач для изоляции тестов"""
    try:
        response = requests.get(f"{base_url}/tasks")
        if response.status_code == 200:
            tasks = response.json()["tasks"]
            for task in tasks:
                requests.delete(f"{base_url}/tasks/{task['id']}")
    except:
        pass  # Игнорируем ошибки при очистке

