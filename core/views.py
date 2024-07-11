from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .forms import FarmerSignUpForm, ConsumerSignUpForm, LoginForm

def home(request):
    return render(request, 'core/home.html')

def farmer_signup(request):
    if request.method == 'POST':
        form = FarmerSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = FarmerSignUpForm()
    return render(request, 'core/signup.html', {'form': form, 'user_type': 'Farmer'})

def consumer_signup(request):
    if request.method == 'POST':
        form = ConsumerSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = ConsumerSignUpForm()
    return render(request, 'core/signup.html', {'form': form, 'user_type': 'Consumer'})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'You have been logged in successfully.')
                return redirect('home')  # Replace 'home' with your desired redirect URL after login
            else:
                messages.error(request, 'Invalid username or password.')
    else:
        form = LoginForm()
    return render(request, 'core/login.html', {'form': form})
    
def logout_view(request):
    logout(request)
    return redirect('home')  # Replace 'home' with the name of your home view or any other URL