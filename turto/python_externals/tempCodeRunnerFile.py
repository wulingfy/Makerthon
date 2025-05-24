g

dass = {
       "stress",
       "anxiety",
       "depression"
}

questions = {
    "stress": [
        "I found it hard to wind down",
        "I tended to over-react to situations",
        "I felt that I was using a lot of nervous energy",
        "I found myself getting agitated",
        "I found it difficult to relax",
        "I was intolerant of anything that kept me from getting on with what I was doing",
        "I felt that I was rather touchy"
    ],
    "anxiety": [
        "I was aware of dryness of my mouth",
        "I experienced breathing difficulty (e.g. excessively rapid breathing, breathlessness in the absence of physical exertion)",
        "I experienced trembling (e.g. in the hands)",
        "I was worried about situations in which I might panic and make a fool of myself",
        "I felt I was close to panic",
        "I was aware of the action of my heart in the absence of physical exertion (e.g. sense of heart rate increase, heart missing a beat)",
        "I felt scared without any good reason"
    ],
    "depression": [
        "I couldn’t seem to experience any positive feeling at all",
        "I found it difficult to work up the initiative to do things",
        "I felt that I had nothing to look forward to",
        "I felt down-hearted and blue",
        "I was unable to become enthusiastic about anything",
        "I felt I wasn’t worth much as a person",
        "I felt that life was meaningless"
    ]
}


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
mental_instruction = """
I have a set of DASS-21 questions
Merge this question and the script to personalize the question example
Limit: 8 Words
- Question: I find it hard to wind down 
- Script: I don't like being in crowded places.
if no relevant:
Output: I find it hard to wind down 
else:
Output: I find it hard to wind down while being in crowded places.
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
       data["accuracy"] = '100%' #chat.send_message(mess).text 
       mess = score_range + user_message
       data["range"] =  '100%' #chat.send_message(mess).text
       mess = score_control + user_message
       data["control"] =  '100%' #chat.send_message(mess).text
       data["fix"] = reply.text
       
       # Mental Health
       return data

def mental_script():
       global user_message
       data = []
       with open('turto/text_data/script.txt', 'r', encoding='utf-8') as file:
              user_message = file.read()
      
       for key in dass:
              for quest in questions[key]:
                     question_start = mental_instruction + "\nQuestion: " + quest + " "
                     question_start = question_start + "Script: " + user_message
                     new_question = chat.send_message(question_start)
                     print(new_question.text)
                     data.append(new_question.text)
       return data
                 


if __name__ == "__main__":
       data = mental_script()
       print(data)