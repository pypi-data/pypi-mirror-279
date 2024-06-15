def edit_task(task_name, new_task_dis):
    import json
    from .settings import tasks, marks, tasks_file, edit_tasks_marks
    tasks2 = tasks()
    marks2 = marks()

    if task_name in tasks:
        tasks2[task_name] = new_task_dis
        with open(tasks_file(), "w") as f:
            json.dump(tasks2, f)
        edit_tasks_marks(tasks2, marks2)

        return 'edited'
    else:
        return 'not_found'