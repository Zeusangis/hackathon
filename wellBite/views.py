from django.shortcuts import render
import requests
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from user.models import BodyMassIndex


@login_required(login_url="login")
def index(request):
    return render(request, "wellBite/index.html")


def choose(request):
    university_api = "http://universities.hipolabs.com"
    universities = []
    q = request.GET.get("query")
    if q:
        response = requests.get(f"{university_api}/search?name={q}")
        if response.status_code == 200:
            universities = response.json()
        else:
            universities = []
    print(universities)
    return render(request, "wellBite/choose.html", {"universities": universities})


def get_university(request):
    university_api = "http://universities.hipolabs.com"
    q = request.GET.get("query")
    universities = []

    if q:
        response = requests.get(f"{university_api}/search?name={q}")
        if response.status_code == 200:
            universities = response.json()

    return JsonResponse(universities, safe=False)


def submit_choices(request):
    if request.method == "POST":
        print("POST")
        university = request.POST.get("university_name")
        selected_plan = request.POST.get("selected_options")
        meal_plan = request.POST.get("meal_plan")
        print(university)
        print(selected_plan)
        print(meal_plan)
    return render(request, "wellBite/index.html")


@login_required(login_url="login")
def about(request):
    return render(request, "wellBite/about.html")


@login_required(login_url="login")
def profile(request):
    user = request.user
    if user.is_authenticated:
        name = user.full_name
        email = user.email
        print("User is authenticated.")
    else:
        print("User is not authenticated.")
    context = {
        "name": name,
        "email": email,
    }

    if request.method == "POST":
        print("POST")
        new_name = request.POST.get("fullName")
        new_email = request.POST.get("email")
        height = request.POST.get("height")
        weight = request.POST.get("weight")
        age = request.POST.get("age")
        gender = request.POST.get("gender")
        print(new_name)

    return render(request, "wellBite/profile.html", context)
