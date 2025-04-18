from pyt2s.services import stream_elements
from playsound import playsound

def voice(text):
    data = stream_elements.requestTTS(text, stream_elements.Voice.Ivy.value) 
    with open('output.mp3', '+wb') as file:
        file.write(data)
    playsound('output.mp3')

#TESTING
# def voice2():
#     data = stream_elements.requestTTS('i love love love love love love love love ngo bao lam', stream_elements.Voice.Ivy.value) 
#     with open('output.mp3', '+wb') as file:
#         file.write(data)
#     playsound('output.mp3')

# voice2()
    