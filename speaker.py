import speech_recognition

audio = speech_recognition.Recognizer()
def get_text():
    with speech_recognition.Microphone() as mic:
        curr_audio = audio.listen(mic)
    try:
        text = audio.recognize_google(curr_audio)
    except:
        text = "error"    
    return text

#Thay thành whisper soon.