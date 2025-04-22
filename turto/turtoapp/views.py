from django.shortcuts import render, HttpResponse

# Create your views here.

def home(request):
    # return HttpResponse("Hello, world!")
    return render(request, "main.html")

def judge(request):
    return render(request, "judge.html")