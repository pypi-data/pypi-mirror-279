def transcribe_audio(filename="recorder.wav"):
    import speech_recognition as sr
    recognizer = sr.Recognizer()
    with sr.AudioFile(filename) as source:
        audio = recognizer.record(source)
        try:
            query = recognizer.recognize_google(audio, language='en-US')
            return query
        except sr.UnknownValueError:
            return ""
        except sr.RequestError as e:
            print (f"Could not request results; {e}")
            return f"Could not request results; {e}"