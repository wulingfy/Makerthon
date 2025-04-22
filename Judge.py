import google.generativeai as genai

genai.configure(api_key="AIzaSyARpFsUQp-xF_YrESLvshU7wkoBWd2iL7Q")
# Gemini - 1.5 - pro
model = genai.GenerativeModel("gemini-1.5-pro")  

# Định nghĩa vai trò bằng prompt hệ thống
system_instruction = """"
       You're a friendly and supportive English teacher. Please correct any grammar mistakes in my spoken English sentences. Keep the tone casual and conversational, and explain why something is wrong in a simple way. Then, show me a more natural way to say it, like how a native speaker would say it. Here's my first sentence
       Example: She don't like coffee but she drink it every morning
       Correction:
       - "She don't like coffee" → "She doesn't like coffee"
       - "she drink it" →  "she drinks it"
       Why:
       - In the present simple tense, we use "doesn't" with "she/he/it", and we add -s to the verb: "drinks".
       Natural version:
       - She doesn\’t like coffee, but she drinks it every morning anyway.
       - type answer using: markdown
"""

chat = model.start_chat()

response = chat.send_message(system_instruction)
response.text

def check_script(mess):
       reply = chat.send_message(mess)
       return reply.text

if __name__ == "__main__":
       fix = check_script("BaoLam are gay")
       print(fix)
