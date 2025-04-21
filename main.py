import speaker 
import processing
import recording

Process = True
keyword = [
    "see you again"
    "bye"
    "quit"
]

def add(full_text,text):
    full_text = full_text + ' ' + text
    return

def turn_off(script):
    for key in keyword:
        if key in script:
            return False
    return True        

import keyboard


if __name__ == "__main__":
    recording.start_conversation()
    keyboard.wait('esc')  # keep script running 
