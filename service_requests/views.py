from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.contrib import messages

# Home page view
def home(request):
    return render(request, 'home.html')

# User Registration view
def register_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        number = request.POST.get('number', '')
        
        # Check if email already exists
        if User.objects.filter(username=email).exists():
            messages.error(request, 'Email is already taken.')
            return redirect('register')
        
        # Create a new user
        user = User.objects.create_user(username=email, password=password, email=email)
        user.profile.phone_number = number  # Assuming you have a profile model for phone number
        user.save()

        # Success message
        messages.success(request, 'You have successfully registered.')
        return redirect('login')

    return render(request, 'register.html')

# User Login view
def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        
        # Authenticate user
        user = authenticate(request, username=email, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, 'You have successfully logged in.')
            return redirect('home')
        else:
            messages.error(request, 'Invalid credentials, please try again.')
            return redirect('login')

    return render(request, 'login.html')
