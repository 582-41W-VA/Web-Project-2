from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .forms import ParentProfileForm, TutorProfileForm, UserRegisterForm, UserLoginForm
from .models import TutorProfile, ParentProfile


def homepage(request):
    tutors = TutorProfile.objects.select_related('user').all()
    return render(request, 'brainboosters/home.html', {'tutors': tutors})


def register(request):
    # Check for the 'user_type' query parameter
    user_type = request.GET.get('user_type', None)

    if request.method == 'POST':
        form = UserRegisterForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user) 

            # Redirect to profile creation based on user type
            if user.user_type == 'tutor':
                return redirect('create_tutor_profile')
            elif user.user_type == 'parent':
                return redirect('create_parent_profile')
    else:
        # Pre-fill the form with the selected user_type
        initial_data = {}
        if user_type:
            initial_data['user_type'] = user_type
        form = UserRegisterForm(initial=initial_data)
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
                return redirect('homepage')
    else:
        form = UserLoginForm()
    return render(request, 'brainboosters/login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('login')


@login_required
def create_tutor_profile(request):
    # Check if the user already has a tutor profile and redirect if profile already exists
    if hasattr(request.user, 'tutor_profile'):
        return redirect('tutor_dashboard')
    
    if request.method == 'POST':
        form = TutorProfileForm(request.POST)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user  # Associate the profile with the logged-in user
            profile.save()

            # Handle the profile picture (saved to the User model)
            if 'profile_picture' in request.FILES:
                request.user.profile_picture = request.FILES['profile_picture']
                request.user.save()

            return redirect('tutor_dashboard')  # Redirect to the tutor dashboard
    else:
        form = TutorProfileForm()
    return render(request, 'brainboosters/create_tutor_profile.html', {'form': form})


@login_required
def create_parent_profile(request):
    # Check if the user already has a parent profile and redirect if profile already exists
    if hasattr(request.user, 'parent_profile'):
        return redirect('parent_dashboard') 
    
    if request.method == 'POST':
        form = ParentProfileForm(request.POST)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user  # Associate the profile with the logged-in user
            profile.save()

            # Handle the profile picture (saved to the User model)
            if 'profile_picture' in request.FILES:
                request.user.profile_picture = request.FILES['profile_picture']
                request.user.save()

            return redirect('parent_dashboard')  # Redirect to the parent dashboard
    else:
        form = ParentProfileForm()
    return render(request, 'brainboosters/create_parent_profile.html', {'form': form})


@login_required
def tutor_dashboard(request):
    # Ensure the user is a tutor
    if request.user.user_type != 'tutor':
        return redirect('home')  # Redirect non-tutors to the home page

    # Fetch the tutor's profile
    tutor_profile = TutorProfile.objects.get(user=request.user)
    return render(request, 'brainboosters/tutor_dashboard.html', {'tutor_profile': tutor_profile})


@login_required
def parent_dashboard(request):
    # Ensure the user is a parent
    if request.user.user_type != 'parent':
        return redirect('home')  # Redirect non-parents to the home page

    # Fetch the parent's profile
    parent_profile = ParentProfile.objects.get(user=request.user)
    return render(request, 'brainboosters/parent_dashboard.html', {'parent_profile': parent_profile})