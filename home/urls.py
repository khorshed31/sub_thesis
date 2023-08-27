from django.urls import path,include
from .import views

urlpatterns = [
    path('',views.home,name="home"),
    path('web_cam', views.web_cam, name="web_cam"),
]