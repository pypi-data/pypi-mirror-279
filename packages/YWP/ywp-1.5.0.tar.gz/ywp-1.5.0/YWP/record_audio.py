import wave
import sounddevice as sd

def record_audio(filename="recorder.wav", duration=5, fs=44100):
    sd.default.device = 2
    try:
        audio_data = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='int16')
        sd.wait()
        with wave.open(filename, 'wb') as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(fs)
            wf.writeframes(audio_data.tobytes())
        return "saved"
    except Exception as e:
        print ("An error occurred:", e)
        return "An error occurred:", e