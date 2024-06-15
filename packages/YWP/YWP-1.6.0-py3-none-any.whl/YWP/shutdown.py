def shutdown():
    import platform
    import subprocess
    system = platform.system()
    if system == "Windows":
        subprocess.run(["shutdown", "/s", "/t", "1"])
    elif system == "Linux" or system == "Darwin":  # Darwin is the system name for macOS
        subprocess.run(["sudo", "shutdown", "-h", "now"])
    else:
        raise NotImplementedError("Unsupported OS")