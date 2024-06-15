import os
import platform

def log_off():
    system = platform.system()
    if system == "Windows":
        os.system("shutdown /l")
    else:
        raise NotImplementedError("Unsupported OS")