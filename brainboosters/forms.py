from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import ParentProfile, TutorProfile, User

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    USER_TYPE_CHOICES = [
        ('tutor', 'Tutor'),
        ('parent', 'Parent'),
    ]
    user_type = forms.ChoiceField(choices=USER_TYPE_CHOICES, widget=forms.RadioSelect)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'user_type']

    def clean_user_type(self):
        user_type = self.cleaned_data.get("user_type")
        if not user_type:
            raise forms.ValidationError("You must select either 'Tutor' or 'Parent'.")
        return user_type

class UserLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))


class TutorProfileForm(forms.ModelForm):
    name = forms.CharField(required=True)
    profile_picture = forms.ImageField(required=False)

    class Meta:
        model = TutorProfile
        fields = ['name', 'gender', 'degree', 'school', 'major', 'experience', 'method', 'hourly_rate', 'description']


class ParentProfileForm(forms.ModelForm):
    name = forms.CharField(required=True)
    profile_picture = forms.ImageField(required=False)

    class Meta:
        model = ParentProfile
        fields = ['name', 'location', 'child_name', 'child_age', 'child_grade']