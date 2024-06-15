def log_off():
    import os
    import platform
    system = platform.system()
    if system == "Windows":
        os.system("shutdown /l")
    else:
        raise NotImplementedError("Unsupported OS")