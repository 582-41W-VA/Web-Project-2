from django.urls import path
from . import views

urlpatterns = [
    path('zoom', views.create_zoom_meeting, name='create_zoom_meeting'),
]
