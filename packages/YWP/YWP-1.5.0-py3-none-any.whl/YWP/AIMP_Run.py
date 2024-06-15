from .open_file import open_file

def AIMP_Run():
    open = open_file("aimp.exe")
    if open == "open":
        print("opened")
    else:
        print("Not Found Path")