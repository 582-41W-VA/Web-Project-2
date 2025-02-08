from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    user_type = models.CharField(
        max_length=10, 
        choices=[
            ('tutor', 'Tutor'),
            ('parent', 'Parent'),
        ],
        null=True, 
        blank=True
    )
    profile_picture = models.ImageField(
        upload_to='profile_pictures/', 
        null=True, 
        blank=True, 
        help_text="Upload a profile picture"
    )
    contact_number = models.CharField(max_length=15, null=True, blank=True)


class TutorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='tutor_profile')
    name = models.CharField(max_length=80, null=True, blank=True)
    gender = models.CharField(max_length=10, choices=[('M', 'Male'), ('F', 'Female')], null=True, blank=True)
    degree = models.CharField(
        max_length=10, 
        choices=[
            ('bachelor', 'Bachelor'),
            ('master', 'Master'),
            ('doctor', 'Doctor'),
        ], 
        null=True, 
        blank=True
    )
    school = models.CharField(max_length=100, null=True, blank=True)
    major = models.CharField(max_length=100, null=True, blank=True)
    experience = models.CharField(max_length=100, null=True, blank=True)
    method = models.CharField(max_length=20, choices=[('in_person', 'In Person'), ('online', 'Online'), ('hybrid', 'Hybrid'),], null=True, blank=True)
    hourly_rate = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    description = models.CharField(max_length=300, null=True, blank=True)

    def __str__(self):
        return self.user.username


class ParentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='parent_profile')
    name = models.CharField(max_length=80, null=True, blank=True)
    location = models.CharField(max_length=255, null=True, blank=True)
    child_name = models.CharField(max_length=50, null=True, blank=True)
    child_age = models.PositiveIntegerField(null=True, blank=True)
    child_grade = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.user.username


class Review(models.Model):
    tutor = models.ForeignKey(TutorProfile, on_delete=models.CASCADE, related_name='tutor_reviews')
    parent = models.ForeignKey(ParentProfile, on_delete=models.CASCADE, related_name='parent_reviews')
    rating = models.PositiveIntegerField()  # e.g., 1-5 stars
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.parent.user.username} for {self.tutor.user.username}"


class Subject(models.Model):
    name = models.CharField(max_length=100, unique=True)
    tutors = models.ManyToManyField(TutorProfile, related_name='subject_list') 

    def __str__(self):
        return self.name


class Level(models.Model):
    name = models.CharField(max_length=100, unique=True)
    tutors = models.ManyToManyField(TutorProfile, related_name='level_list') 

    def __str__(self):
        return self.name