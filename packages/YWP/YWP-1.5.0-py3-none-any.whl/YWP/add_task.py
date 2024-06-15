import json
from .settings import *

def add_task(task_name, task_dis):
    tasks2 = tasks()
    marks2 = marks()

    tasks2[task_name] = task_dis
    marks2[task_name] = "no"
    with open(tasks_file(), "w") as f:
        json.dump(tasks2, f)
    with open(marks_file(), "w") as f:
        json.dump(marks2, f)

    edit_tasks_marks(tasks2, marks2)

    return 'added'