from django.db import models

# Create your models here.
class Video(models.Model):
    user_id = models.IntegerField()
    title = models.CharField(max_length=255)
    video_file = models.FileField(upload_to='videos/')  # This will store the video file in the 'media/videos/' directory
    upload_date = models.DateTimeField(auto_now_add=True)
