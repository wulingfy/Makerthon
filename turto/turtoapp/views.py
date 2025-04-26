from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from python_externals import recording
from python_externals import processing
from python_externals import tts
from django.views.decorators.csrf import csrf_exempt
import json

# Create your views here.

def home(request):
    # return HttpResponse("Hello, world!")
    return render(request, "main.html")

def judge(request):
    return render(request, "judge.html")

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
