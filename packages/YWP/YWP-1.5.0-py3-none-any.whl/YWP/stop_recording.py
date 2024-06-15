import pyaudio

def stop_recording():
    p = pyaudio.PyAudio()
    for i in range(p.get_device_count()):
        p.terminate()