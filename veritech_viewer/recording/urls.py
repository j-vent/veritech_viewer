from django import views
from django.urls import path
from recording import views
urlpatterns = [
    path('', views.recording_home, name='recording'),
    path('edit/', views.edit_booklet, name='edit'),
]