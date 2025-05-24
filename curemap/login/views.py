import base64
from django.core.files.base import ContentFile
from django.contrib.auth import authenticate, login , logout
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from .forms import RegisterUserForm
from django.core.mail import send_mail
from django.conf import settings  # Ensure you have EMAIL settings in settings.py



# Create your views here.

########    USER LOGIN, REGISTRATION AND LOGOUT FUNCTIONS   ######## 

def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request,user)
            messages.success(request,("loggin in successfully"))
            return redirect('homepage')
        else:
            messages.success(request,("There was an error in loggin In , Try Again.."))
            return redirect('login_user')
    else:
       return render(request, 'loginpage/login.html') 
        

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .forms import RegisterUserForm

def register_user(request):
    if request.method == "POST":
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password1']

            # Send email after registration
            send_mail(
                subject="Welcome to CureMap!",
                message=f"Hi {username},\n\nThanks for registering at CureMap.\nWe're happy to have you!",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[email],
                fail_silently=False,
            )

            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "Registration successful")
                return redirect('homepage')
            else:
                messages.error(request, "Authentication failed")
        else:
            messages.error(request, "Form is invalid")
    else:
        form = RegisterUserForm()

    return render(request, 'loginpage/register.html', {'form': form})


def logout_user(request):
    logout(request)
    messages.success(request, ("You have been logged out successfully."))
    return redirect('homepage')