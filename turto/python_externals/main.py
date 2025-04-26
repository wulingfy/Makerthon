import speaker 
import processing
import recording
import keyboard
import grammar_judge
import threading
storage_chat = []
is_recording = False

def response_bot(text):
    print("USER: " + text)
    storage_chat.append(text)
    reply  = processing.response(text)
    print("BOT: " + reply)

def start_conversation():
    threading.Thread(target=main_loop, daemon=True).start() # loop

def main_loop():
    while True:
        keyboard.wait('space')
        if not recording.is_recording:
            recording.start_recording()
        else:
            print('DONE RECORDING, RESPONDING')
            text = recording.stop_recording()
            with open('text_data/script.txt', 'w', encoding='utf-8') as file:
                file.write(text) 
            response_bot(text)
        # Wait for release
        keyboard.wait('space', suppress=True)

def judging():
    for script in storage_chat:
        reply = grammar_judge.check_script(script)
        with open('text_data/reply.txt', 'a', encoding='utf-8') as file:
            file.write(reply + '\n')

if __name__ == "__main__":
    start_conversation() 
    keyboard.wait('esc')
    if is_recording:
        recording.stop_recording()
    judging()
