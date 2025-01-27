from django.shortcuts import render
from django.http import JsonResponse
from .zoom_service import generate_zoom_meeting

def create_zoom_meeting(request):
    meeting = generate_zoom_meeting()
    if meeting:
        return JsonResponse({
            'join_url': meeting['join_url'],
            'start_url': meeting['start_url'],
            'meeting_id': meeting['meeting_id'],
        })
    else:
        return JsonResponse({'error': 'Failed to create meeting'}, status=500)

# from .models import Tutor, Appointment

# def tutor_list(request):
#     tutors = Tutor.objects.all()
#     return render(request, 'tutors/tutor_list.html', {'tutors': tutors})

# def appointment_detail(request, appointment_id):
#     appointment = Appointment.objects.get(id=appointment_id)
#     return render(request, 'tutors/appointment_detail.html', {'appointment': appointment})

