import os
from django.conf import settings
from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from python_externals import recording
from python_externals import assessment
from python_externals import processing
from python_externals import tts
from python_externals import grammar_judge
from django.views.decorators.csrf import csrf_exempt
import json

# Create your views here.

SCRIPT_FILE_PATH = os.path.join(settings.BASE_DIR, 'text_data', 'script.txt')
REPLY_FILE_PATH = os.path.join(settings.BASE_DIR, 'text_data', 'reply.txt')
DATA_FILE_PATH = os.path.join(settings.BASE_DIR, 'text_data', 'data_pronunciation.csv')

def home(request):
    try:
        # Open the file in write mode to clear its contents
        with open(SCRIPT_FILE_PATH, 'w') as file:
            file.truncate(0)  # This clears the file content
        with open(DATA_FILE_PATH, 'w') as file:
            file.truncate(0)  # This clears the file content

        # Now render your page
        return render(request, 'main.html')  # Change the template name accordingly

    except Exception as e:
        print(f"Error while clearing the file: {e}")
        # Optionally, handle errors if needed
        return render(request, 'error_page.html')  # Render an error page or some fallback

def judge(request):
    grammar_judge.check_script()
    # pronun = convert_xml.get_data_pronunciation()

    #Define the file path
    file_path = os.path.join('text_data', 'reply.txt')
    
    #Read the content of the text file
    try:
        with open(file_path, 'r') as file:
            file_content = file.read()
    except FileNotFoundError:
        file_content = "File not found."

    # Pass the content to the template
    # return render(request, 'judge.html', {'file_content': file_content, 'pronun': pronun})
    return render(request, 'judge.html', {'file_content': file_content})

@csrf_exempt
def start_recording_view(request):
    try:
        recording.start_recording()  # Call your start_recording function
        return JsonResponse({'status': 'success'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})

# View to handle stopping the recording
@csrf_exempt
def stop_recording_view(request):
    try:
        transcription = recording.stop_recording()  # Call your stop_recording function
        return JsonResponse({'status': 'success', 'transcription': transcription})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})

# View to handle responding
@csrf_exempt
def response_view(request):
    try:
        data = json.loads(request.body)
        user_message = data.get('user_message')
        respond = processing.response(user_message)  # Call your function
        return JsonResponse({'status': 'success', 'respond': respond})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})
    
@csrf_exempt
@csrf_exempt
def text_to_speech_view(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            text = data.get('text')

            if not text:
                return JsonResponse({'status': 'error', 'message': 'No text provided'}, status=400)

            tts.voice(text)  # <-- Make sure playsound() is correct

            return JsonResponse({'status': 'success'})

        except Exception as e:
            print("Error in text_to_speech_view:", e)
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)


# View to start the conversation
@csrf_exempt
def start_view(request):
    try:
        respond = processing.start()  # Call your function
        return JsonResponse({'status': 'success', 'respond': respond})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})
    