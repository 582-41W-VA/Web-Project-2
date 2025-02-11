from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from .forms import ContactForm, ParentProfileForm, TutorProfileForm, UserRegisterForm, UserLoginForm,TutorSearchForm
from .models import TutorProfile, Review, ParentProfile
import random


def homepage(request):
    tutors = list(TutorProfile.objects.select_related('user').all())  # Convert queryset to a list
    random_tutors = random.sample(tutors, 3) if len(tutors) >= 3 else tutors  # Pick 3 random tutors
    
    return render(request, 'brainboosters/home.html', {'tutors': random_tutors})


def register(request):
    # Check for the 'user_type' query parameter
    user_type = request.GET.get('user_type', None)

    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
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

def tutor_search(request):
    tutors = TutorProfile.objects.all()
    
    if request.method == "POST":
        form = TutorSearchForm(request.POST)

        if form.is_valid():
            subject = form.cleaned_data.get("subject")
            level = form.cleaned_data.get("level")
            price = form.cleaned_data.get("price")
            gender = form.cleaned_data.get("gender")
            method = form.cleaned_data.get("filter_method")

            if subject:
                tutors = tutors.filter(major=subject)  
            if level is not None:
                tutors = tutors.filter(degree=level)  
            if price is not None:
                tutors = tutors.filter(hourly_rate=price)
            if gender is not None:
                tutors = tutors.filter(gender=gender) 
            if method is not None:
                tutors = tutors.filter(method=method) 

    
    else:
        form = TutorSearchForm()

    return render(request, 'brainboosters/search.html', {"tutors": tutors})


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
    try:
        tutor_profile = TutorProfile.objects.get(user=request.user)
        return render(request, 'brainboosters/tutor_dashboard.html', {'tutor_profile': tutor_profile})
    except ObjectDoesNotExist:
        return redirect('create_tutor_profile')


@login_required
def parent_dashboard(request):
    # Ensure the user is a parent
    if request.user.user_type != 'parent':
        return redirect('home')  # Redirect non-parents to the home page

    # Fetch the parent's profile
    try:
        parent_profile = ParentProfile.objects.get(user=request.user)
        return render(request, 'brainboosters/parent_dashboard.html', {'parent_profile': parent_profile})
    except ObjectDoesNotExist:
        return redirect('create_parent_profile')


@login_required
def edit_tutor_profile(request, pk):
    profile = get_object_or_404(TutorProfile, pk=pk, user=request.user)
    if request.method == 'POST':
        form = TutorProfileForm(request.POST, instance=profile)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()

            # Handle the profile picture (saved to the User model)
            if 'profile_picture' in request.FILES:
                request.user.profile_picture = request.FILES['profile_picture']
                request.user.save()

            return redirect('tutor_dashboard')
    else:
        form = TutorProfileForm(instance=profile)
    return render(request, 'brainboosters/edit_tutor_profile.html', {'form': form})


@login_required
def edit_parent_profile(request, pk):
    profile = get_object_or_404(ParentProfile, pk=pk, user=request.user)
    if request.method == 'POST':
        form = ParentProfileForm(request.POST, instance=profile)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()

            # Handle the profile picture (saved to the User model)
            if 'profile_picture' in request.FILES:
                request.user.profile_picture = request.FILES['profile_picture']
                request.user.save()

            return redirect('parent_dashboard')
    else:
        form = ParentProfileForm(instance=profile)
    return render(request, 'brainboosters/edit_parent_profile.html', {'form': form})


@login_required
def tutor_detail(request, tutor_id):
    tutor = get_object_or_404(TutorProfile, id=tutor_id)
    reviews = tutor.tutor_reviews.all()

    if request.method == 'POST':
        if 'submit_review' in request.POST:
            rating = request.POST.get('rating')
            comment = request.POST.get('comment')
            parent_profile = ParentProfile.objects.get(user=request.user)
            Review.objects.create(tutor=tutor, parent=parent_profile, rating=rating, text=comment)
            return redirect('tutor_detail', tutor_id=tutor_id)
        elif 'submit_contact' in request.POST:
            contact_form = ContactForm(request.POST)
            if contact_form.is_valid():
                return redirect('tutor_detail', tutor_id=tutor_id)
    else:
        contact_form = ContactForm()

    context = {
        'tutor': tutor,
        'reviews': reviews,
        'contact_form': contact_form,
    }
    return render(request, 'brainboosters/tutor_detail.html', context)