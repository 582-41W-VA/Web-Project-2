from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import ParentProfile, TutorProfile, User

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    USER_TYPE_CHOICES = [
        ('tutor', 'Tutor'),
        ('parent', 'Parent'),
    ]
    user_type = forms.ChoiceField(choices=USER_TYPE_CHOICES, widget=forms.RadioSelect, required=False)

    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput,
        help_text='Your password must be at least 8 characters long and contain both letters and numbers.'
    )
    password2 = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput,
        help_text='Enter the same password as above, for verification.'
    )

    class Meta:
        model = User
        fields = ['username', 'user_type', 'email', 'password1', 'password2']

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
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
    ]

    DEGREE_CHOICES = [
        ('Bachelor', 'Bachelor'),
        ('Master', 'Master'),
        ('Ph.D.', 'Ph.D.'),
    ]

    METHOD_CHOICES = [
        ('Online', 'Online'),
        ('In-Person', 'In-Person'),
        ('Online & In-Person', 'Online & In-Person'),
    ]

    gender = forms.ChoiceField(choices=GENDER_CHOICES, required=True, widget=forms.Select(attrs={'class': 'form-control'}))
    degree = forms.ChoiceField(choices=DEGREE_CHOICES, required=True)
    method = forms.ChoiceField(choices=METHOD_CHOICES, required=True)

    class Meta:
        model = TutorProfile
        fields = ['name', 'gender', 'degree', 'school', 'major', 'experience', 'method', 'hourly_rate', 'description']


class ParentProfileForm(forms.ModelForm):
    name = forms.CharField(required=True)
    profile_picture = forms.ImageField(required=False)

    class Meta:
        model = ParentProfile
        fields = ['name', 'location', 'child_name', 'child_age', 'child_grade']


# class ContactForm(forms.Form):
#     name = forms.CharField(max_length=100)
#     email = forms.EmailField()
#     message = forms.CharField(widget=forms.Textarea)

class ContactForm(forms.Form):
    first_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'placeholder': 'First Name'}))
    last_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'placeholder': 'Last Name'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Email'}))
    message = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Message'}))
