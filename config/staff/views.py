from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Staff
from .forms import StaffRegistrationForm


def register_view(request):
    """
    Handle staff registration.

    If the request method is POST, it processes the registration form.
    If valid, it saves the new staff member and redirects to the login page.

    Args:
        request: The HTTP request object.

    Returns:
        Rendered registration page or redirects to login on success.
    """
    if request.method == "POST":
        form = StaffRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Staff registered successfully!")
            return redirect("login")  # Redirect to the login page or wherever you want
    else:
        form = StaffRegistrationForm()
    return render(request, "staff/register.html", {"form": form})


def login_view(request):
    """
    Handle staff login.

    If the request method is POST, it authenticates the user with the provided email and password.
    If valid, it logs in the user and redirects to the home page.

    Args:
        request: The HTTP request object.

    Returns:
        Rendered login page or redirects to home on successful login.
    """
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            print(f"Failed login attempt for email: {email}")
            messages.error(request, "Invalid email or password.")
    return render(request, "staff/login.html")


@login_required
def logout_view(request):
    """
    Handle staff logout.

    Logs out the user and redirects to the login page.

    Args:
        request: The HTTP request object.

    Returns:
        Redirect to the login page.
    """
    logout(request)
    return redirect("login")


def home_view(request):
    """
    Render the home page for logged-in staff members.

    Args:
        request: The HTTP request object.

    Returns:
        Rendered home page.
    """
    return render(request, "staff/home.html")


@login_required
def staff_view(request):
    """
    Display a list of all staff members.

    Args:
        request: The HTTP request object.

    Returns:
        Rendered staff list page with all staff members.
    """
    staff_members = Staff.objects.all()
    return render(request, "staff_list.html", {"staff_members": staff_members})
