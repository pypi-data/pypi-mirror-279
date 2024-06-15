def load_tasks():
    import json
    from .settings import tasks_file, marks_file, edit_tasks_marks
    tasks_file2 = tasks_file()
    marks_file2 = marks_file()

    with open (tasks_file2, "w") as file:
        tasks2 = json.load(file)
    
    with open (marks_file2, "w") as file:
        marks2 = json.load(file)

    tasks = tasks2
    marks = marks2

    edit_tasks_marks(tasks, marks)

    return 'loaded'