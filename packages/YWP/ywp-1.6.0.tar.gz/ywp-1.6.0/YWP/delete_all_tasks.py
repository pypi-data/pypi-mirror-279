def delete_all_tasks():
    import json
    from .settings import tasks_file, marks_file, edit_tasks_marks
    tasks = {}
    marks = {}

    with open (tasks_file(), "w") as file:
        json.dump(tasks, file)
    
    with open (marks_file(), "w") as file:
        json.dump(marks, file)

    edit_tasks_marks(tasks, marks)

    return 'deleted'