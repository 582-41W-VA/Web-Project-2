from django.urls import path
from . import views

urlpatterns = [
    path('jitsi', views.jitsi_meeting_view, name='jitsi_meeting_view'),
]

