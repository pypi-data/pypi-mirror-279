def task_mark_done(task_name, new_mark="yes"):
    import json
    from .settings import tasks, marks, marks_file, edit_tasks_marks
    tasks2 = tasks()
    marks2 = marks()

    if new_mark == "yes" or new_mark == "no":
        a = 0
    else:
        return 'not marked'
    if task_name in tasks2:
        marks2[task_name] = new_mark
        with open(marks_file(), "w") as f:
            json.dump(marks2, f)
        edit_tasks_marks(tasks2, marks2)
        
        return 'marked'
    else:
        return 'not found'