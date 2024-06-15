import os
import subprocess

# Define the path to aimp.exe
aimp_path = "../aimp.exe"

# Check if the file exists
if os.path.exists(aimp_path):
    # Open aimp.exe using subprocess.Popen
    subprocess.Popen(aimp_path)
else:
    print("File not found:", aimp_path)
