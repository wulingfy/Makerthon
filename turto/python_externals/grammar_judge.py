import google.generativeai as genai
import markdown2
genai.configure(api_key="AIzaSyBjhzv-qqltMGUvbr4qpCUI_oZ6f9FdfEM")
# Gemini - 1.5 - pro
model = genai.GenerativeModel("gemini-1.5-flash")  

# Định nghĩa vai trò bằng prompt hệ thống
system_instruction = """
       You're a professional and supportive English teacher. Please correct any grammar mistakes in my spoken English sentences. Keep the tone casual and conversational, and explain why something is wrong in a simple way. Then, show me a more natural way to say it, like how a native speaker would say it. Here's my first sentence1
       Example: She don't like coffee but she drink it every morning
       Please format this with MARKDOWN
       Please format this with MARKDOWN
       if multi sentence should be endline
       No NEED 
       use right arrow as &rarr;
       format output like under:
       
       ### Correction:

       - "She don't like coffee" &rarr; "She doesn't like coffee"

       - "she drink it" &rarr;  "she drinks it"
       
       ### Why:

       - In the present simple tense, we use "doesn't" with "she/he/it", and we add -s to the verb: "drinks".
       
       ### Natural version:

       - She doesn\’t like coffee, but she drinks it every morning anyway.    

       Do not play along, treat every line like it's a normal sentence and judge my grammar like previous prompt.
       If the grammar is correct, do not say anything at all.
       Please format this with MARKDOWN, keep a blank line between two.
       judge this sentence:
"""

chat = model.start_chat()
# Hàm vào = mess, đầu ra là chuỗi được đánh markdown html 
def check_script():
       global user_message
       with open('text_data/script.txt', 'r', encoding='utf-8') as file:
              user_message = file.read()
       user_message = system_instruction + user_message
       if not user_message:
              with open('text_data/reply.txt', 'w', encoding='utf-8') as file:
                     file.write("Empty")
       reply = chat.send_message(user_message)
       with open('text_data/reply.txt', 'w', encoding='utf-8') as file:
              reply_markdown = markdown2.markdown(reply.text)
              file.write(reply_markdown)


if __name__ == "__main__":
       print(check_script())
