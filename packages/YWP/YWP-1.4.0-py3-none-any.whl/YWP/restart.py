import os
import platform

def restart():
    system = platform.system()
    if system == "Windows":
        os.system("shutdown /r /t 1")
    else:
        raise NotImplementedError("Unsupported OS")