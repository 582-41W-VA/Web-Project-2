from django.shortcuts import render
from .jitsi_service import generate_meeting_id

def jitsi_meeting_view(request):
    meeting_id = generate_meeting_id()
    jitsi_url = f'https://meet.jit.si/{meeting_id}' 
    return render(request, 'jitsi_meeting.html', {'jitsi_url': jitsi_url})


