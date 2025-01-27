# tutors/zoom_service.py
import jwt
import requests
import datetime
from django.conf import settings

API_KEY = settings.ZOOM_API_KEY
API_SECRET = settings.ZOOM_API_SECRET

def generate_zoom_meeting():
    # generate JWT token
    payload = {
        'iss': API_KEY,
        'exp': int(datetime.datetime.utcnow().timestamp()) + 5000  # expires in 5 seconds
    }
    
    jwt_token = jwt.encode(payload, API_SECRET, algorithm='HS256')

    # Zoom API endpoint
    url = 'https://api.zoom.us/v2/users/me/meetings'
    
    # Meeting details
    meeting_data = {
        "topic": "Tutoring Session",  
        "type": 2,  #meeting type: 2 for scheduled meeting
        "start_time": "2025-01-30T10:00:00Z",
        "duration": 30,
        "timezone": "UTC",
        "agenda": "Tutoring session discussion",
        "settings": {
            "host_video": True, #meeting host video
            "participant_video": True,  #participant video
            "audio": "voip",  #meeting audio
            "auto_recording": "cloud"  #meeting recording
        }
    }

    headers = {
        'Authorization': f'Bearer {jwt_token}',
        'Content-Type': 'application/json'
    }

    # Send POST request
    response = requests.post(url, json=meeting_data, headers=headers)

    if response.status_code == 201:
        meeting_info = response.json()
        # return meeting details
        return {
            'join_url': meeting_info['join_url'],  # meeting join link
            'start_url': meeting_info['start_url'],  # meeting start link
            'meeting_id': meeting_info['id'],  # meeting id
        }
    else:
        print(f"Error creating Zoom meeting: {response.status_code}")
        print(response.json())
        return None
