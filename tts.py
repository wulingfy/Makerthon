from pyt2s.services import stream_elements
from playsound import playsound

def voice(text):
    data = stream_elements.requestTTS(text, stream_elements.Voice.Ivy.value) 
    with open('aivoice.mp3', '+wb') as file:
        file.write(data)
    playsound('aivoice.mp3')

if __name__ == "__main__":
    print("TEST")


    
