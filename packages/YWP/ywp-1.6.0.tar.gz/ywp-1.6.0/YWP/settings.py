import os
import json

setting_file = "settings.json"
tasks_file = "tasks.json"
marks_file = "marks.json"
tasks = {}
marks = {}
files = {}

if os.path.exists(tasks_file):
    with open(tasks_file, "r") as f:
        tasks = json.load(f)

if os.path.exists(marks_file):
    with open(marks_file, "r") as f:
        marks = json.load(f)

def tasks():
    if os.path.exists(tasks_file):
        with open(tasks_file, "r") as f:
            tasks = json.load(f)
    else:
        tasks = {}
    return tasks

def marks():
    if os.path.exists(marks_file):
        with open(marks_file, "r") as f:
            marks = json.load(f)
    else:
        marks = {}
    return marks

def tasks_file():
    return tasks_file

def marks_file():
    return marks_file

def edit_tasks_marks(tasks_tasks, marks_marks):
    global tasks
    global marks
    
    tasks = tasks_tasks
    marks = marks_marks
    return "edited"
