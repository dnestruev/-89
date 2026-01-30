import json
import os
from datetime import datetime

TASKS_FILE = "tasks.json"

# ======================== Загрузка и сохранение ========================
def load_tasks():
    if not os.path.exists(TASKS_FILE):
        return []
    with open(TASKS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_tasks(tasks):
    with open(TASKS_FILE, "w", encoding="utf-8") as f:
        json.dump(tasks, f, ensure_ascii=False, indent=2)

# ======================== Основные функции ========================
def add_task(text):
    tasks = load_tasks()
    task = {
        "id": len(tasks) + 1,
        "text": text,
        "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "done": False
    }
    tasks.append(task)
    save_tasks(tasks)
    print(f"✅ Задача добавлена: {text}")

def complete_task(task_id):
    tasks = load_tasks()
    for task in tasks:
        if task["id"] == task_id:
            task["done"] = True
            save_tasks(tasks)
            print(f"✔️ Задача выполнена: {task['text']}")
            return
    print("❌ Задача не найдена")

def list_tasks(show_done=True, keyword=None):
    tasks = load_tasks()
    for task in tasks:
        if not show_done and task["done"]:
            continue
        if keyword and keyword.lower() not in task["text"].lower():
            continue
        status = "✅" if task["done"] else "❌"
        print(f"{task['id']}. {task['text']} [{status}] ({task['date']})")

def help_menu():
    print("""
📌 Команды:
add <текст>       - Добавить задачу
done <id>         - Отметить задачу выполненной
list              - Показать все задачи
list pending      - Показать только невыполненные
search <слово>    - Поиск по задачам
help              - Показать эту справку
exit              - Выйти
""")

# ======================== CLI интерфейс ========================
def main():
    print("=== TaskManager v1.0 ===")
    help_menu()
    while True:
        command = input("\nВведите команду: ").strip()
        if command.startswith("add "):
            add_task(command[4:])
        elif command.startswith("done "):
            try:
                complete_task(int(command[5:]))
            except ValueError:
                print("❌ Нужно число ID задачи")
        elif command == "list":
            list_tasks()
        elif command == "list pending":
            list_tasks(show_done=False)
        elif command.startswith("search "):
            list_tasks(keyword=command[7:])
        elif command == "help":
            help_menu()
        elif command == "exit":
            print("👋 Пока!")
            break
        else:
            print("❌ Неизвестная команда, напиши 'help' для списка команд")

if __name__ == "__main__":
    main()

