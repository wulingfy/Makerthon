import google.generativeai as genai
import markdown2
genai.configure(api_key="AIzaSyARpFsUQp-xF_YrESLvshU7wkoBWd2iL7Q")
# Gemini - 1.5 - pro
model = genai.GenerativeModel("gemini-1.5-pro")  

# Định nghĩa vai trò bằng prompt hệ thống
system_instruction = """"
       You're a professional and supportive English teacher. Please correct any grammar mistakes in my spoken English sentences. Keep the tone casual and conversational, and explain why something is wrong in a simple way. Then, show me a more natural way to say it, like how a native speaker would say it. Here's my first sentence1
       Example: She don't like coffee but she drink it every morning
       Please format this with Markdown.
       format output like under:
       Correction:
       - "She don't like coffee" → "She doesn't like coffee"
       - "she drink it" →  "she drinks it"
       Why:
       - In the present simple tense, we use "doesn't" with "she/he/it", and we add -s to the verb: "drinks".
       Natural version:
       - She doesn\’t like coffee, but she drinks it every morning anyway.    
"""

chat = model.start_chat()

response = chat.send_message(system_instruction)
response.text
# Hàm vào = mess, đầu ra là chuỗi được đánh markdown html 
def check_script(mess):
       reply = chat.send_message(mess)
       return markdown2.markdown(reply.text)

if __name__ == "__main__":
       fix = check_script("I is handsome")
       fix = markdown2.markdown(fix)
       print(fix)
