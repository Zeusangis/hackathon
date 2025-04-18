from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import login, logout, authenticate
from .models import CustomUser as User
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from django.contrib import messages


def user_login(request):
    if request.user.is_authenticated:
        return redirect("index")
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect("index")
        else:
            messages.error(request, "Invalid Credentials!")
            return redirect("login")
    return render(request, "user/login.html")


def user_register(request):
    if request.user.is_authenticated:
        return redirect("index")
    if request.method == "POST":
        name = request.POST["name"]
        email = request.POST["email"]
        password = request.POST["password"]
        cpassword = request.POST["cpassword"]

        if cpassword != password:
            messages.error(request, "Passwords do not match!")
            return redirect("register")

        try:
            user = User(full_name=name, email=email)
            user.set_password(password)  # Hash the password here
            user.save()
        except IntegrityError:
            messages.error(request, "Email is already taken.")
            return redirect("register")

        login(request, user)
        return redirect("index")
    return render(request, "user/register.html")


@login_required(login_url="login")
def user_logout(request):
    logout(request)
    return redirect(reverse("login"))
