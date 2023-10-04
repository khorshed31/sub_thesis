from typing import Counter
from django.http.response import HttpResponse
from django.shortcuts import redirect, render
import cv2
import os
import numpy as np
from django.shortcuts import render
from django.http import JsonResponse
import tensorflow as tf
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import FileSystemStorage
import logging
from django.conf import settings
from django.contrib import messages

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


def results_page(request):
    analysis_result = request.session.get('analysis_result', None)
    therapy_name = request.session.get('therapy_name', None)

    if analysis_result is not None:
        # Remove the analysis_result from the session to clear it
        request.session.pop('analysis_result', None)
        request.session.pop('therapy_name', None)

        # Render the results template and pass the analysis result
        return render(request, 'report.html', {'analysis_result': analysis_result, 'therapy_name' : therapy_name})
    else:
        # If analysis_result is not found in the session, show an error message
        messages.error(request, 'Analysis result not found.')
        return redirect('upload_video')   
    

# Define the exercise_to_model_mapping dictionary
exercise_to_model_mapping = {
    "e1": "home/physiotherapy_models/e1.h5",
    "e2": "home/physiotherapy_models/e2.h5",
    "e3": "home/physiotherapy_models/e3.h5",
    "e4": "home/physiotherapy_models/e4.h5",
    "e5": "home/physiotherapy_models/e5.h5",
    "e6": "home/physiotherapy_models/e6.h5",
    "e7": "home/physiotherapy_models/e7.h5",
    "e8": "home/physiotherapy_models/e8.h5",
}    
    

def load_pretrained_model(model_path):
    try:
        model = tf.keras.models.load_model(model_path)
        return model
    except Exception as e:
        # Handle any exceptions that may occur during model loading
        print(f"Error loading the model: {str(e)}")
        return None    

# Load the pre-trained model
# model = load_pretrained_model('home/physiotherapy_models/e1.h5')    

 # Only for demonstration; use CSRF protection in production.
@csrf_exempt
def upload_video(request):
    if request.method == 'POST' and request.FILES.get('video'):
        video = request.FILES['video']
        therapy_name = request.POST.get('therapy_name', '') 
        fs = FileSystemStorage(location='media/')
        custom_name = 'video.webm'
        filename = fs.save(custom_name, video)

        #  # Ensure that the exercise_type is valid (i.e., it exists in your mapping)
        # if exercise_type not in exercise_to_model_mapping:
        #     return JsonResponse({'error': 'Invalid exercise type.'}, status=400)

         # Ensure that the exercise_type is valid (i.e., it exists in your mapping)
        if therapy_name not in exercise_to_model_mapping:
            return JsonResponse({'error': 'Invalid exercise type.'}, status=400)

        # Construct the file path to the uploaded video
        media_root = settings.MEDIA_ROOT
        video_file_path = os.path.join(media_root, filename)
        if video_file_path:
            # Process the video with the pre-trained model
            analysis_result = process_video(video_file_path, therapy_name)
            # Store the analysis result in the session
            request.session['analysis_result'] = analysis_result
            request.session['therapy_name'] = therapy_name
            # Return the analysis result as JSON
            return JsonResponse({'result': analysis_result})
            # return redirect('results_page')
        else:
            return JsonResponse({'error': 'No video file uploaded.'})

    return JsonResponse({'message': 'Invalid request'}, status=400)

def process_video(video_file, exercise_type):
    sequence_frames = []  # Collect frames for a sequence
    sequence_length = 35  # Define the desired sequence length
    highest_probability_class = None

    # Load the selected model based on the exercise type
    model_path = exercise_to_model_mapping.get(exercise_type)

    if model_path:
        selected_model = load_pretrained_model(model_path)

        if selected_model:
            sequence_frames = []  # Collect frames for a sequence
            sequence_length = 35  # Define the desired sequence length
            highest_probability_class = None

            cap = cv2.VideoCapture(video_file)

            while True:
                ret, frame = cap.read()
                if not ret:
                    break

                # Preprocess the frame
                processed_frame = preprocess_frame(frame)

                # Append the preprocessed frame to the sequence
                sequence_frames.append(processed_frame)

                # If we have collected enough frames for a sequence, process it
                if len(sequence_frames) == sequence_length:
                    sequence_result, highest_probability_class = process_sequence(sequence_frames, selected_model)
                    break  # Exit the loop after processing the first sequence

            cap.release()

            # Delete the video file once processing is complete
            os.remove(video_file)

            return sequence_result, highest_probability_class
        
        # Handle the case where the selected model couldn't be loaded or exercise_type is not found
    return None, None


def process_sequence(frames, model):
    # Process the sequence of frames using the selected model
    try:
        # Preprocess the sequence if needed
        preprocessed_sequence = preprocess_sequence(frames)

        # Run the preprocessed sequence through the selected model
        predictions = model.predict(np.array([preprocessed_sequence]))

        # Process the model's predictions and return the analysis result as well as the highest probability class
        analysis_result, highest_probability_class = post_process_predictions(predictions)

        return analysis_result, highest_probability_class

    except Exception as e:
        return f"Error during sequence processing: {str(e)}", None

def preprocess_sequence(frames):
    # Preprocess the entire sequence of frames as needed
    # You may need to apply operations like resizing, normalization, or any other preprocessing steps
    # Ensure that the input shape matches your model's expectations
    
    preprocessed_frames = [preprocess_frame(frame) for frame in frames]

    # Combine the preprocessed frames to form the sequence
    preprocessed_sequence = np.array(preprocessed_frames)

    return preprocessed_sequence

def preprocess_frame(frame):
    # Preprocess an individual frame (e.g., resize, normalize, etc.) as per your model's requirements
    # Example: Resize the frame to a specific size
    resized_frame = cv2.resize(frame, (128, 128))
    
    # You may need to apply further preprocessing steps here, such as normalizing pixel values
    
    return resized_frame

def post_process_predictions(predictions):
    # Define class labels (replace with your actual class labels)
    class_labels = ["Class 0", "Class 1", "Class 2", "Class 3", "Class 4"]

    # Initialize variables to keep track of the highest probability class and its probability
    highest_probability_class = None
    highest_probability = -1  # Initialize with a very low value

    # Initialize an empty list to store the formatted results
    formatted_results = []

    # Iterate through the predictions and format them
    for i, pred in enumerate(predictions[0]):
        class_label = class_labels[i]
        probability = pred * 100  # Convert probability to percentage
        formatted_result = f"{class_label}: {probability:.2f}%"
        formatted_results.append(formatted_result)

        # Check if the current class has a higher probability than the previous highest
        if probability > highest_probability:
            highest_probability = probability
            highest_probability_class = class_label

    # Join the formatted results into a single string
    analysis_result = " ".join(formatted_results)

    return analysis_result, highest_probability_class