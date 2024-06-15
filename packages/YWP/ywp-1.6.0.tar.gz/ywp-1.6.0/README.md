# YWP Package

A big Package has a lot of things From Your Wanted Products (YWP)

## Installation

You can install this package using pip:
```
pip install YWP
```
## Usage

```python
from YWP import play_audio(pro_path, mp3_audio_file)
from YWP import stop_recording()
from YWP import create_file(name) :
    name : the name of the file
    body : show in cmd with input
from YWP import open_file(filepath)
from YWP import open_website(url)
from YWP import shutdown()
from YWP import record_audio(filename='recorder.wav')
from YWP import transcribe_audio(filename='recorder.wav')
from YWP import text_to_speech(text, filename="tts.mp3", language='en')
from YWP import play_sound(filename='tts.mp3')
from YWP import restart()
from YWP import log_off()
from YWP import hibernate()
from YWP import play_audio_online(pro_path, mp3_file_link) :
    pro_path : any program can run online audio like AIMP
from YWP import token_information(data, type='binance') :
    Supported Types Now:
        1- binance
        2- etherum
        3- geckoterminal
    data required:
        1- binance (token)
        2- etherum (token)
        3- geckoterminal (pool)
from YWP import add_task(task_name, task_dis)
from YWP import delete_all_tasks()
from YWP import delete_task(task_name)
from YWP import edit_mark_done_task(task_name, new_mark="yes") :
    new_mark values:
        yes
        no
from YWP import edit_tasks(task_name, new_task_dis)
from YWP import load_tasks()
from YWP import delete_task(task_name)
from YWP import tasks()
from YWP import marks()
from YWP import tasks_file()
from YWP import marks_file()
from YWP import all_tasks()
from YWP import edit_tasks_marks(tasks_tasks, marks_marks)
from YWP import route_flask(location, returnValue)
from YWP import run(check=False, debug=True, host="0.0.0.0", port="8000")
from YWP import train(jsonfile="intents.json", picklefile="data.pickle", h5file="model.h5")
from YWP import process(message="", picklefile="data.pickle", h5file="model.h5", jsonfile="intents.json", sleeptime=0)
from YWP import json_creator(jsonfile="intents.json", tag="", patterns=[], responses=[])
from YWP import basic_video_creator(image_folder="images/", animation_choice="None", frame_rate=25, video_name="output", video_type=".mp4", video_platform="Youtube", image_time=5):
    Available Platforms:
        1- Youtube
        2- Tiktok
        3- Instagram
        4- Facebook
    Available Animations:
        1- FadeIn
        2- FadeOut
        3- Rotate
        4- FlipHorizontal
        5- FlipVertical
        6- None
```

### LICENSE

MIT License
```
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

...
```