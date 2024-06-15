def play_audio_online(pro_path, mp3_file_link):
        import subprocess
        # قم بتشغيل AIMP وتمرير الملف الصوتي إليه
        subprocess.Popen([pro_path, mp3_file_link])
        return "opened"