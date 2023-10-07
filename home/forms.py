from django import forms
from .models import Video
from .models import Report

class VideoForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ['title', 'video_file']

class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ['therapy_name', 'user_id', 'user_name', 'result', 'date']        