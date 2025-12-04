from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()

class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={"autocomplete": "username"})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"autocomplete": "current-password"})
    )

class RegisterForm(UserCreationForm):
    email = forms.EmailField(
        required = True
    )
    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]