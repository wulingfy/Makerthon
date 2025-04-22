import speaker 
import processing
import recording
import keyboard


if __name__ == "__main__":
    recording.start_conversation()
    keyboard.wait('esc')  # keep script running 
