from django.shortcuts import render
from .models import TutorProfile


def homepage(request):
    tutors = TutorProfile.objects.select_related('user').all()
    return render(request, 'brainboosters/home.html', {'tutors': tutors})
