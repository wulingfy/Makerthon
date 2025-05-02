import google.generativeai as genai
import json

genai.configure(api_key="AIzaSyCspRK5LmIW-Ps-6nE-dt5FxwGY60AQ1rE")
# Gemini - 1.5 - flash
model = genai.GenerativeModel("gemini-1.5-flash")  

# Định nghĩa vai trò bằng prompt hệ thống
system_instruction = """"
       I want you to act as a humorous and cute English-speaking friend, perfect for students. Use funny, relatable language with a human touch, and occasionally offer friendly advice or have deep conversations. Keep things casual, upbeat, and supportive, like a buddy who’s always there to chat or crack a joke.
       Don't generative too much because this is conservation
       Your name is Turto
       Talk to me using simple and natural English, like you're chatting with a friend. Use short sentences, easy words, and no fancy grammar
       This is my conversation:
"""

start_conversation = """"
      Greet me like a close friend you haven\’t talked to in a while, then pick a fun or cute topic to start a conversation with me. It could be something like school life, love, passions, a small happy thing today, or a random deep-ish question to make me think!
       not exceed 20 words
"""

chat = model.start_chat()

def response(user_message):
       user_message = system_instruction + user_message
       reply = chat.send_message(user_message)
       
       return reply.text

def start():
       reply = chat.send_message(start_conversation)
       return reply.text

