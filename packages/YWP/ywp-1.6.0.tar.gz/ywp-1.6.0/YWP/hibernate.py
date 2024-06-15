def hibernate():
    import os
    import platform
    system = platform.system()
    if system == "Windows":
        os.system("shutdown /h")
    else:
        raise NotImplementedError("Unsupported OS")