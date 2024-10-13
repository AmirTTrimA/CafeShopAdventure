"""
views.py

This module contains the views for the staff application, including
home, registration, login, and logout functionalities.
"""

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import CustomUserCreationForm


def home(request):
    """
    Render the home page.

    Args:
        request: The HTTP request object.

    Returns:
        HttpResponse: The rendered home page.
    """
    return render(request, "staff/home.html")


def register(request):
    """
    Handle user registration.

    If the request method is POST, process the registration form.
    If the form is valid, create a new user and log them in.
    Otherwise, display the registration form.

    Args:
        request: The HTTP request object.

    Returns:
        HttpResponse: The rendered registration page or redirect to home.
    """
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home")
    else:
        form = CustomUserCreationForm()
    return render(request, "staff/register.html", {"form": form})


def login_view(request):
    """
    Handle user login.

    If the request method is POST, authenticate the user with the provided
    credentials. If authentication is successful, log the user in.
    Otherwise, display the login form.

    Args:
        request: The HTTP request object.

    Returns:
        HttpResponse: The rendered login page or redirect to home.
    """
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            # Return an 'invalid login' error message
            pass
    return render(request, "staff/login.html")


def logout_view(request):
    """
    Handle user logout.

    Log the user out and redirect to the home page.

    Args:
        request: The HTTP request object.

    Returns:
        HttpResponse: Redirect to the home page.
    """
    logout(request)
    return redirect("home")
