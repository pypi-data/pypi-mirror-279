import os
import subprocess

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