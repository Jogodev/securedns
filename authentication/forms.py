from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.forms import AuthenticationForm

class LoginForm(AuthenticationForm):
    email = forms.EmailField(max_length=254, label=_("Email"), widget=forms.TextInput(attrs={
            "class": "form-control form-control-user",
            "id": "exampleInputEmail",
            "aria-describedby": "emailHelp",
            "placeholder": "Enter Email Address..."
    }))
    password = forms.CharField(label=_('Mot de passe'), widget=forms.PasswordInput(attrs={
        "class": "form-control form-control-user",
        "id": "exampleInputPassword",
            "aria-describedby": "emailHelp",
            "placeholder": "Confirm password"
        }))
    
class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=63, label="Prénom", widget=forms.TextInput(attrs={
            "class": "form-control form-control-user",
            "id": "exampleLastName",
            "placeholder": "First Name"
        }))
    last_name = forms.CharField(max_length=63, label="Nom", widget=forms.TextInput(attrs={
            "class": "form-control form-control-user",
            "id": "exampleLastName",
            "placeholder": "Last Name"
        }))
    email = forms.EmailField(max_length=254, label="Email", widget=forms.TextInput(attrs={
        "class": "form-control form-control-user home_form_input",
        "id": "exampleInputEmail",
        "aria-describedby": "emailHelp",
        "placeholder": "Enter Email Address..."
    }))
    password1 = forms.CharField(max_length=63, widget=forms.PasswordInput(attrs={
            "class": "form-control form-control-user",
            "id": "exampleInputPassword",
            "aria-describedby": "emailHelp",
            "placeholder": "Password"
        }))
    password2 = forms.CharField(
        max_length=63,
        widget=forms.PasswordInput(attrs={
            "class": "form-control form-control-user",
            "id": "exampleInputPassword",
            "placeholder": "Confirm password"
        }))

    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ['last_name', 'first_name', 'email', 'password1', 'password2']
        
class HomeForm(forms.Form):
    dns = forms.CharField(max_length=100, required=False,  widget=forms.TextInput(attrs={
            "class": "form-control form-control-user home_form_input",
            "id": "exampleInputEmail",
            "aria-describedby": "emailHelp",
            "placeholder": "Enter a domain"
    }))
