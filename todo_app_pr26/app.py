from flask import Flask, render_template, request, redirect
import json
import os
from datetime import datetime

app = Flask(__name__)

FILE_NAME = "tasks.json"


def load_tasks():
    """Загрузка задач из JSON-файла."""
    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, "r", encoding="utf-8") as file:
            return json.load(file)
    return []


def save_tasks(tasks):
    """Сохранение задач в JSON-файл."""
    with open(FILE_NAME, "w", encoding="utf-8") as file:
        json.dump(tasks, file, ensure_ascii=False, indent=2)


tasks = load_tasks()


@app.route("/")
def index():
    return render_template("index.html", tasks=tasks)


@app.route("/add", methods=["POST"])
def add_task():
    task_text = request.form.get("task", "").strip()

    if task_text:
        task = {
            "text": task_text,
            "created_at": datetime.now().strftime("%d.%m.%Y %H:%M")
        }
        tasks.append(task)
        save_tasks(tasks)

    return redirect("/")


@app.route("/delete/<int:task_id>")
def delete_task(task_id):
    if 0 <= task_id < len(tasks):
        tasks.pop(task_id)
        save_tasks(tasks)

    return redirect("/")


@app.route("/clear")
def clear_tasks():
    tasks.clear()
    save_tasks(tasks)
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
