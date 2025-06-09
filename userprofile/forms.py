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
        labels = {
            "address": "Адрес",
            "phone_number": "Номер телефона", 
            "userphoto": "Фото профиля"
        }
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

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if phone_number:
            cleaned_phone = ''.join(filter(str.isdigit, phone_number))
            
            if not cleaned_phone.startswith('380'):
                raise forms.ValidationError("Phone number should start with +380")
            
            if len(cleaned_phone) != 12:
                raise forms.ValidationError("Invalid phone number")
            
            return f"+{cleaned_phone}"
        
        return phone_number
    
    def clean_address(self):
        address = self.cleaned_data.get('address')
        if address and len(address) < 10:
            raise forms.ValidationError("Address is too short")
        return address