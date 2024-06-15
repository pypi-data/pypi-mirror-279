def play_audio(pro_path, mp3_file_path):
    import os
    import subprocess
    if os.path.exists(mp3_file_path):
        # قم بتشغيل AIMP وتمرير الملف الصوتي إليه
        subprocess.Popen([pro_path, mp3_file_path])
        return "opened"
    else:
        return "Not Found File"