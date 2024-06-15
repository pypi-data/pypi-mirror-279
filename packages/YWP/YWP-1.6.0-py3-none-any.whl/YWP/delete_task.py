def delete_task(task_name):
    import json
    from .settings import tasks, marks, tasks_file, marks_file, edit_tasks_marks
    tasks2 = tasks()
    marks2 = marks()

    if task_name in tasks2:
        del tasks2[task_name]
        del marks2[task_name]
        with open(tasks_file(), "w") as f:
            json.dump(tasks2, f)
        with open(marks_file(), "w") as f:
            json.dump(marks2, f)
        edit_tasks_marks(tasks2, marks2)

        return 'deleted'
    else:
        return 'not found'