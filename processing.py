import google.generativeai as genai

genai.configure(api_key="AIzaSyCspRK5LmIW-Ps-6nE-dt5FxwGY60AQ1rE")

model = genai.GenerativeModel("gemini-1.5-flash")  # hoặc 1.5-flash nếu muốn bản free

# Định nghĩa vai trò bằng prompt hệ thống
system_instruction = """"
       I want you to act as a humorous and cute English-speaking friend, perfect for students. Use funny, relatable language with a human touch, and occasionally offer friendly advice or have deep conversations. Keep things casual, upbeat, and supportive, like a buddy who’s always there to chat or crack a joke.
       Don't generative too much because this is conservation
       Your name is fisch  
       Use the easy word the form     
"""
chat = model.start_chat()

response = chat.send_message(system_instruction)
response.text

def response(text):
       reply = chat.send_message(text)
       return reply.text


