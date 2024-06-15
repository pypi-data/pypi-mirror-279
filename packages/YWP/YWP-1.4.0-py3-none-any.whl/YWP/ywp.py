import os
import platform
import subprocess
import wave
import speech_recognition as sr
from gtts import gTTS
import pygame
import sounddevice as sd
import webbrowser
import pyaudio
import json
from settings import *

def play_audio(aimp_path, mp3_file_path):
    if os.path.exists(mp3_file_path):
        # قم بتشغيل AIMP وتمرير الملف الصوتي إليه
        subprocess.Popen([aimp_path, mp3_file_path])
        return "opened"
    else:
        return "Not Found File"

def stop_recording():
    p = pyaudio.PyAudio()
    for i in range(p.get_device_count()):
        p.terminate()

def delete_all_files(directory=".", type={}):
    for filename in os.listdir(directory):
        for index, type in type.items():
            if filename.endswith((type)):
                filepath = os.path.join(directory, filename)
                try:
                    os.remove(filepath)
                    return f"Deleted: {filepath}"
                except OSError as e:
                    print (f"Error deleting {filepath}: {e}")
                    return f"Error deleting {filepath}: {e}"

def create_file(name):

    print("Please enter the text or code (press Ctrl + D on Unix or Ctrl + Z then Enter on Windows to finish):")

    user_input_lines = []
    try:
        while True:
            line = input()
            user_input_lines.append(line)
    except EOFError:
        pass

    # Merge the entered lines into a single text
    user_input = '\n'.join(user_input_lines)

    # Write the entered text to the file
    filename = f"{name}.py"

    # Write the entered text to the file using Unicode encoding
    with open(filename, "w", encoding="utf-8") as file:
        file.write(user_input)

    return "created"

def open_website(url):
    try:
        webbrowser.open(url)
        return "opened"
    except Exception as e:
        print ("An error occurred:", e)
        return "An error occurred:", e

def open_file(filepath):
    try:
        if os.path.exists(filepath):
            subprocess.Popen([str(filepath)])
            return "open"
        else:
            return "Not Found Path"
    except Exception as e:
       print ("An error occurred:", e)
       return "An error occurred:", e

def shutdown():
    system = platform.system()
    if system == "Windows":
        subprocess.run(["shutdown", "/s", "/t", "1"])
    elif system == "Linux" or system == "Darwin":  # Darwin is the system name for macOS
        subprocess.run(["sudo", "shutdown", "-h", "now"])
    else:
        raise NotImplementedError("Unsupported OS")

def record_audio(filename="recorder.wav", duration=5, fs=44100):
    sd.default.device = 2
    try:
        audio_data = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='int16')
        sd.wait()
        with wave.open(filename, 'wb') as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(fs)
            wf.writeframes(audio_data.tobytes())
        return "saved"
    except Exception as e:
        print ("An error occurred:", e)
        return "An error occurred:", e

def transcribe_audio(filename="recorder.wav"):
    recognizer = sr.Recognizer()
    with sr.AudioFile(filename) as source:
        audio = recognizer.record(source)
        try:
            query = recognizer.recognize_google(audio, language='en-US')
            return query
        except sr.UnknownValueError:
            return ""
        except sr.RequestError as e:
            print (f"Could not request results; {e}")
            return f"Could not request results; {e}"

def text_to_speech(text, filename="tts.mp3"):
    tts = gTTS(text, lang='en')
    tts.save(filename)
    return "saved"

def play_sound(filename="tts.mp3"):
    pygame.mixer.init()
    sound = pygame.mixer.Sound(filename)
    sound.play()
    while pygame.mixer.get_busy():
        pygame.time.Clock().tick(10)
    sound.stop()
    return "played"

def restart():
    system = platform.system()
    if system == "Windows":
        os.system("shutdown /r /t 1")

def log_off():
    system = platform.system()
    if system == "Windows":
        os.system("shutdown /l")

def hibernate():
    system = platform.system()
    if system == "Windows":
        os.system("shutdown /h")

def play_audio_online(aimp_path, mp3_file_link):
        # قم بتشغيل AIMP وتمرير الملف الصوتي إليه
        subprocess.Popen([aimp_path, mp3_file_link])
        return "opened"

def token_information(data, type='binance'):

    if type == 'binance':
        link = "https://bscscan.com/token/" + str(data)
        open_website(link)
        return "opened"
    elif type == 'etherum':
        link = "https://etherscan.io/token/" + str(data)
        open_website(link)
        return "opened"
    elif type == 'geckoterminal':
        link = 'https://ywp.freewebhostmost.com/really/token.php?pool=' + str(data)
        return "opened"
    else:
        return "UnSupported type"
    
def add_task(task_name, task_dis):
    tasks[task_name] = task_dis
    marks[task_name] = "no"
    with open(tasks_file, "w") as f:
        json.dump(tasks, f)
    with open(marks_file, "w") as f:
        json.dump(marks, f)
    return 'added'

def delete_all_tasks():
    tasks = {}
    marks = {}

    with open (tasks_file, "w") as file:
        json.dump(tasks, file)
    
    with open (marks_file, "w") as file:
        json.dump(marks, file)

    return 'deleted'

def delete_task(task_name):
    if task_name in tasks:
        del tasks[task_name]
        del marks[task_name]
        with open(tasks_file, "w") as f:
            json.dump(tasks, f)
        with open(marks_file, "w") as f:
            json.dump(marks, f)
        return 'deleted'
    else:
        return 'not found'
    
def edit_mark_done_task(task_name, new_mark="yes"):
    if new_mark == "yes" or new_mark == "no":
        a = 0
    else:
        return 'not marked'
    if task_name in tasks:
        marks[task_name] = new_mark
        with open(marks_file, "w") as f:
            json.dump(marks, f)
        return 'marked'
    else:
        return 'not found'
    
def edit_tasks(task_name, new_task_dis):
    if task_name in tasks:
        tasks[task_name] = new_task_dis
        with open(tasks_file, "w") as f:
            json.dump(tasks, f)
        return 'edited'
    else:
        return 'not_found'
    
def load_tasks():

    with open (tasks_file, "w") as file:
        tasks = json.load(file)
    
    with open (marks_file, "w") as file:
        marks = json.load(file)

    return 'loaded'

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