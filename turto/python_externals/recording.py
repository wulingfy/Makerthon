import os
import sounddevice as sd
import soundfile as sf
import keyboard
import threading
from . import speaker
from . import processing
from . import tts

fs = 16000
channels = 1
# filename = 'audio_data/output.wav'

# Ensure the 'audio_data' directory exists at the root level
audio_data_dir = os.path.join(os.getcwd(), 'audio_data')

# Create the directory if it doesn't exist
if not os.path.exists(audio_data_dir):
    os.makedirs(audio_data_dir)

# Define the path to the file in the 'audio_data' folder
filename = os.path.join(audio_data_dir, 'output.wav')


is_recording = False
stream = None
file = None

def start_recording():
    global is_recording, stream, file 

    try:
        file = sf.SoundFile(filename, mode='w', samplerate=fs, channels=channels)
        stream = sd.InputStream(samplerate=fs, channels=channels, callback=lambda indata, frames, time_info, status: file.write(indata))
        stream.start()  
        is_recording = True
        print("Recording Started")
    except Exception as e:
        print(f"Error opening {filename}: {str(e)}")

def stop_recording() -> str:
    global is_recording, stream, file

    if stream:
        stream.stop()
        stream.close()
    if file:
        file.close()
    is_recording = False
    print("Done recording, save to", filename)
    text = speaker.get_text() # get text
    with open("text_data/script.txt", "a") as file:
        file.write(text + '\n')
    # print("PRESS SPACE TO START/STOP")    
    return text

# def main_loop():
#     global is_recording
#     while True:
#         keyboard.wait('space')
#         if not is_recording:
#             start_recording()
#         else:
#             stop_recording()
#         # Wait for release
#         keyboard.wait('space', suppress=True)

# def start_conversation():
#     threading.Thread(target=main_loop, daemon=True).start() # loop

# EXIT
if __name__ == "__main__":
    print("TEST")