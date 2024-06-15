def stop_recording():
    import pyaudio
    p = pyaudio.PyAudio()
    for i in range(p.get_device_count()):
        p.terminate()