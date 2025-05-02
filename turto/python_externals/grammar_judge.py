import google.generativeai as genai
import markdown2
genai.configure(api_key="AIzaSyCH9m3oRpPxs9atqF1sHxHkEyYPNbF3NNo")
# Gemini - 1.5 - pro
model = genai.GenerativeModel("gemini-1.5-flash")  

# Định nghĩa vai trò bằng prompt hệ thống
system_instruction = """
      [You're a professional and supportive English teacher. Please correct any grammar mistakes in my spoken English sentences. Keep the tone casual and conversational, and explain why something is wrong in a simple way. Then, show me a more natural way to say it, like how a native speaker would say it. Here's my first sentence1
       Example: She don't like coffee but she drink it every morning
       using endline
       format output like under:]

       She don't like coffee: She doesn't like coffee

       she drink it: she drinks it

       In the present simple tense, we use "doesn't" with "she/he/it", and we add -s to the verb: "drinks".

       She doesn\’t like coffee, but she drinks it every morning anyway.    

       [Do not play along, treat every line like it's a normal sentence and judge my grammar like previous prompt.
       If the grammar is correct, do not say anything at all.
       judge all sentence:]
"""

score_accuracy = """
You are an IELTS English-speaking examiner specializing in grammar accuracy.
Your task is to evaluate the following speaking script and give a Grammar Accuracy score from 0 to 100.
Criteria:
       Focus only on grammatical correctness (ignore vocabulary, pronunciation, fluency, or content).

       Minor grammatical errors reduce the score slightly.

       Major errors that affect understanding reduce the score significantly.

       Repeated errors lower the score more than isolated ones.

       A perfect script (0 errors) gets 100.
Output format: only number (score out of 100) 
Script to evaluate:
"""

score_range = """
You are an IELTS Speaking examiner specializing in grammar evaluation.
Your task is to assess the Grammar Range of the following speaking script and give a score from 0 to 100.

Criteria:
       Score the conversation based on the lexical resources user used (like IELTS).
       Low scores will be given if the answers are too short.
       
       Focus only on the variety and complexity of grammatical structures used (ignore accuracy, vocabulary, fluency, or pronunciation).
       The word should be in the hard level ex: supercalifragilisticexpialidocious, or Specialized vocabulary
      
       A wide range of sentence types (simple, compound, complex), verb forms, clauses, conditionals, modals, passive voice, etc., should receive a higher score.
   
       Repeated use of simple structures will lower the score.

Output format: only number (score out of 100)
Script to evaluate:
"""

score_control = """
       You are an IELTS English-speaking examiner specializing in grammar evaluation.
       Your task is to assess the Grammar Control of the following speaking script and give a score from 0 to 100.

              Definition: Grammar Control means the speaker’s ability to consistently use correct grammar, and when errors occur, they self-correct or maintain overall control of meaning.

       Scoring Criteria:

              Focus on how well the speaker manages grammar usage in real-time speech (e.g., consistency, ability to avoid breakdowns, rare or self-corrected errors).

              Occasional slips that do not interfere with communication = small penalty.   

              Frequent errors or major breakdowns in grammar control = big penalty.

       A perfectly controlled script (0 slips, smooth structure) = 100 points.

       Output Format: only number (score out of 100)
       Script to evaluate:
"""

score_mood_expression = """
You are an expert in mental health analysis.
Given the following transcript, assess the speaker's mood negativity on a scale from 0 to 100, where:

0 means extremely positive mood (e.g., joy, hope, calmness, emotional balance),

50 means emotionally neutral or flat,

100 means extremely negative mood (e.g., hopelessness, despair, emotional numbness, signs of depression).

Consider tone, emotional expressions, and word choices. Provide only a numeric score.
Transcript:
"""

score_thinking = """
You are a mental health assessment expert.
Analyze the transcript below and assess the level of negative thinking patterns shown by the speaker.
Consider patterns such as:

Overgeneralization (e.g., “I always fail”)

Catastrophizing (e.g., “This will ruin everything”)

Self-blame or guilt (e.g., “It’s all my fault”)

Hopelessness or black-and-white thinking (e.g., “Nothing will ever get better”)

Negative assumptions about self or others

Score from 0 to 100, where:

0 = no signs of negative thinking

50 = moderate presence of negative thought patterns

100 = pervasive and extreme negative thinking

Return only the numeric score.
Transcript:
"""

give_advice = """
You are a compassionate and professional mental health counselor.
Based on the following transcript, provide personalized, supportive advice that:

Addresses the speaker’s emotional state and thought patterns

Is empathetic and non-judgmental

Offers gentle suggestions or coping strategies (e.g., journaling, reaching out to others, seeing a therapist, self-care tips)

Encourages hope and self-compassion

Keep the advice in a warm, human tone (not robotic), and avoid giving medical diagnoses.
Keep it under 50 words.

Transcript:
"""

chat = model.start_chat()
# Hàm vào = mess, đầu ra là chuỗi được đánh markdown html 
def check_script():
       global user_message
       data = {}
       with open('text_data/script.txt', 'r', encoding='utf-8') as file:
              user_message = file.read()
       user_message = system_instruction + user_message
       if not user_message:
              return data
       # Grammar
       reply = chat.send_message(user_message)
       mess = score_accuracy + user_message
       data["accuracy"] = chat.send_message(mess).text
       mess = score_range + user_message
       data["range"] =  chat.send_message(mess).text
       mess = score_control + user_message
       data["control"] =  chat.send_message(mess).text
       data["fix"] = reply.text

       # Mental Health
       mess = score_mood_expression + user_message
       data["mood_expression"] =  chat.send_message(mess).text
       mess = score_thinking + user_message
       data["thinking"] = chat.send_message(mess).text
       mess = give_advice + user_message
       data["advice"] = chat.send_message(mess).text
       return data


if __name__ == "__main__":
       data = check_script()
       print(data)
