from django.urls import path,include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',views.home,name="home"),
    path('web_cam', views.web_cam, name="web_cam"),
    path('upload_video', views.upload_video, name="upload_video"),
    path('results_page', views.results_page, name='results_page'),
    path('create_report', views.save_form_data, name='create_report'),
    path('my_reports', views.my_reports, name='my_reports'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)