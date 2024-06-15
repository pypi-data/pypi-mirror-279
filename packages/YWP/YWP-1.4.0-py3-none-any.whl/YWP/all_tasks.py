import json
from .settings import *
from .load_tasks import *

def all_tasks():
    load_tasks()

    return {"tasks": tasks(), "marks": marks()}