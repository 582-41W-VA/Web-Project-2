from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User

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


class TutorSearchForm(forms.Form):     
    subject = forms.CharField(required=False, label="Subject")
    level = forms.CharField(required=False, label="CharField")
    price = forms.DecimalField(required=False, label="Price")
    gender = forms.CharField(required=False, label="Gender")
    method = forms.CharField(required=False, label="Method")