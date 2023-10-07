from django.db import models

# Create your models here.
class Video(models.Model):
    user_id = models.IntegerField()
    title = models.CharField(max_length=255)
    video_file = models.FileField(upload_to='videos/')  # This will store the video file in the 'media/videos/' directory
    upload_date = models.DateTimeField(auto_now_add=True)



class Report(models.Model):
    therapy_name = models.CharField(max_length=255)
    user_id = models.IntegerField()
    user_name = models.CharField(max_length=255)
    result = models.DecimalField(max_digits=10, decimal_places=2) 
    date = models.CharField(max_length=255)   
