import os
import platform

def hibernate():
    system = platform.system()
    if system == "Windows":
        os.system("shutdown /h")
    else:
        raise NotImplementedError("Unsupported OS")