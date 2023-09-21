from typing import Counter
from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from account.models import user
from .models import Video
import cv2
import os
import tempfile
import numpy as np
from django.shortcuts import render
from django.http import JsonResponse
from tensorflow import keras
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

# Create your views here.
def home(request):
    # Check if the user is authenticated
    if request.user.is_authenticated:
        user_info = {
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'email': request.user.email,
            # Include any other user-related data you need
        }
    else:
        user_info = None

    return render(request, 'home.html', {'user_info': user_info})


def web_cam(request):
    therapy_name = request.GET.get('therapy_name', '')
    time = request.GET.get('time', '')

    context = {
        'therapy_name': therapy_name,
        'time': time,
    }

    return render(request,'web_cam.html', context)


# Load your pre-trained .h5 model
# Load the pre-trained model
model = keras.models.load_model('E:\Django\SUB\home\physiotherapy_models\e1.h5')

@csrf_exempt  # Only for demonstration; use CSRF protection in production.
def upload_video(request):
    if request.method == 'POST' and request.FILES.get('video'):
        uploaded_video = request.FILES['video']
        filename = 'recorded_video.webm'  # Define the filename for the uploaded video
        file_path = os.path.join('media', filename)  # Save the video in the media folder

        # Save the uploaded video using Django's default storage (media folder)
        default_storage.save(file_path, ContentFile(uploaded_video.read()))
        print(file_path)
        return JsonResponse({'message': 'Video uploaded successfully'})
    return JsonResponse({'message': 'Invalid request'}, status=400)

    