from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserRegisterForm, UserLoginForm
from .models import TutorProfile, ParentProfile


def homepage(request):
    tutors = TutorProfile.objects.select_related('user').all()
    return render(request, 'brainboosters/home.html', {'tutors': tutors})


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()

            # Determine if the user is a tutor or a parent
            user_type = form.cleaned_data.get("user_type")
            if user_type == "tutor":
                TutorProfile.objects.create(user=user)
            elif user_type == "parent":
                ParentProfile.objects.create(user=user)

            messages.success(request, 'Your account has been created. You can log in now.')
            #login(request, user)  # Auto-login after registration
            return redirect("login")
    else:
        form = UserRegisterForm()
    return render(request, 'brainboosters/register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                if user.user_type == "tutor":
                    return redirect('homepage')  # Replace with the tutor panel URL
                elif user.user_type == "parent":
                    return redirect('homepage')  # Replace with the parent panel URL
        messages.error(request, 'Invalid username or password.')
    else:
        form = UserLoginForm()
    return render(request, 'brainboosters/login.html', {'form': form})

def user_logout(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('login')
