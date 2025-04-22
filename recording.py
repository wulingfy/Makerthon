import sounddevice as sd
import soundfile as sf
import keyboard
import threading
import speaker
import processing
import tts

fs = 16000
channels = 1
filename = 'audio_data/output.wav'

is_recording = False
stream = None
file = None

def start_recording():
    global is_recording, stream, file 

    file = sf.SoundFile(filename, mode='w', samplerate=fs, channels=channels)
    stream = sd.InputStream(samplerate=fs, channels=channels, callback=lambda indata, frames, time_info, status: file.write(indata))
    stream.start()  
    is_recording = True
    print("Recording Started")

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
    # with open("text_data/script.txt", "w") as file:
    #     file.write(text)
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
