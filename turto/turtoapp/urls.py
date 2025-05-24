from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings
# from python_externals import main_html

urlpatterns = [
    path('', views.home, name='home'),
    path('start/', views.start_view, name='start'),
    path('judge/', views.judge, name='judge'),
    path('mental-quiz/', views.mental_quiz_view, name='mental_quiz'),
    # path('mental-res/', views.mental_res_view, name='mental_res'),
    path('start-recording/', views.start_recording_view, name='start_recording'),
    path('stop-recording/', views.stop_recording_view, name='stop_recording'),
    path('response/', views.response_view, name='response'),
    path('text-to-speech/', views.text_to_speech_view, name='text_to_speech'),
    path('submit-sliders/', views.submit_sliders, name='submit_sliders'),
    path('result/', views.result_page, name='result'),
]

# urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

