from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User, UserProfile


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(
        label="Username",
        widget=forms.TextInput(attrs={"class": "form-input", "placeholder": " "}),
    )
    email = forms.EmailField(
        label="E-mail",
        widget=forms.EmailInput(attrs={"class": "form-input", "placeholder": " "}),
    )
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={"class": "form-input", "placeholder": " "}),
    )
    password2 = forms.CharField(
        label="Password confirmation",
        widget=forms.PasswordInput(attrs={"class": "form-input", "placeholder": " "}),
    )

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for fieldname in ["username", "password1", "password2"]:
            if fieldname in self.fields:
                self.fields[fieldname].help_text = None


class SignInForm(AuthenticationForm):
    username = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(
            attrs={
                "class": "form-input",
                "placeholder": " ",
                "required": True,
                "autocomplete": "email",
            }
        ),
    )
    password = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-input",
                "placeholder": " ",
                "required": True,
                "autocomplete": "current-password",
            }
        ),
    )


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ["address", "phone_number", "userphoto"]
        widgets = {
            "address": forms.TextInput(
                attrs={"class": "form-input", "placeholder": " "}
            ),
            "phone_number": forms.TextInput(
                attrs={"class": "form-input", "placeholder": " "}
            ),
            "userphoto": forms.FileInput(
                attrs={"class": "form-input", "accept": "image/*"}
            ),
        }
