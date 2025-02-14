from django.contrib import admin
from .models import Level, ParentProfile, TutorProfile, Review, Subject, User
from django.contrib.auth.admin import UserAdmin

# Register the User model with Django's built-in UserAdmin
admin.site.register(User, UserAdmin)
admin.site.register(ParentProfile)
admin.site.register(TutorProfile)
admin.site.register(Review)
admin.site.register(Subject)
admin.site.register(Level)