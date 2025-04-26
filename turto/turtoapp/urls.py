from django.urls import path
from . import views
# from python_externals import main_html

urlpatterns = [
    path('', views.home, name='home'),
    path('judge/', views.judge, name='judge'),
    path('start-recording/', views.start_recording_view, name='start_recording'),
    path('stop-recording/', views.stop_recording_view, name='stop_recording'),
    path('response/', views.response_view, name='response'),
    path('text-to-speech/', views.text_to_speech_view, name='text_to_speech'),
]