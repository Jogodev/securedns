from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.contrib import messages

from . import forms

def signup(request):
    form = forms.SignUpForm()
    if request.method == 'POST':
        form = forms.SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(settings.LOGIN_REDIRECT_URL)
    return render(request, "authentication/signup.html", context={"form": form})   


def login(request):
    form = forms.LoginForm()
    message = ""
    if request.method == 'POST':
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                email = form.cleaned_data["email"],
                password = form.cleaned_data["password"],
            )
            if user is not None:
                login(request, user)
                messages.success(request, f"Bonjour {user.first_name}")
                return redirect(settings.LOGIN_REDIRECT_URL)
            else: 
                message = "Identifiants invalides."
    return render(
        request, "authentication/login.html", context={"form": form, "message": message}
    )            

def logout_user(request):
    """logout_user"""
    logout(request)
    return redirect("home")  

def home(request):
    form = forms.HomeForm()
    if request.method == 'POST':
        form = forms.HomeForm(request.POST)
        if form.is_valid():
            domain = form.cleaned_data['domain']
            

            
            # faire un appel pour verifier la dispo du dns dans notre base
    return render(request, "authentication/home.html", context={'form': form})