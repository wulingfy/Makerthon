import sounddevice as sd
import soundfile as sf
import keyboard
import threading
import speaker
import processing

fs = 44100
channels = 1
filename = 'output.wav'

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

def stop_recording():
    global is_recording, stream, file

    if stream:
        stream.stop()
        stream.close()
    if file:
        file.close()
    is_recording = False
    print("Done recording, save to", filename)
    text = speaker.get_text() # get text
    print("USER: " + text) # trả text   
    reply = processing.response(text) # response AI
    print("BOT: " + reply) # trả response
    print("PRESS SPACE TO START/STOP")

print("PRESS SPACE TO START/STOP")  
def main_loop():
    global is_recording
    while True:
        keyboard.wait('space')
        if not is_recording:
            start_recording()
        else:
            stop_recording()
        # Wait for release
        keyboard.wait('space', suppress=True)

def start_conversation():
    threading.Thread(target=main_loop, daemon=True).start() # loop

# EXIT
if __name__ == "__main__":
    start_conversation() 
    keyboard.wait('esc')
    if is_recording:
        stop_recording()
