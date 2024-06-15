from gtts import gTTS

def text_to_speech(text, filename="tts.mp3", language='en'):
    tts = gTTS(text, lang=language)
    tts.save(filename)
    return "saved"