from pyt2s.services import stream_elements
from playsound import playsound
import os
def voice(text):
    data = stream_elements.requestTTS(text, stream_elements.Voice.Ivy.value) 
    with open("audio_data/aivoice.mp3", '+wb') as file:
        file.write(data)
    playsound("audio_data/aivoice.mp3")
    os.remove("audio_data/aivoice.mp3")

if __name__ == "__main__":
    voice("Hey! It's Turto, not Chad. Nice to meet you! Yeah, I can hear you loud and clear. What's *your* name?")
    voice("I'm gay nice to meet you")
