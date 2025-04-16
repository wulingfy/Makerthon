import speaker 
import processing

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

text = speaker.get_text()

print("USER: " + text)
reply = processing.response(text)
print("BOT: " + reply)
