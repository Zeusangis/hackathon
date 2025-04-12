from django.shortcuts import render, redirect
import requests
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

from user.models import CustomUser, BodyMassIndex


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


def calculate_bmi(height_cm, weight_kg):
    """
    Calculates BMI and returns a tuple (bmi, category).
    """
    try:
        height_cm = float(height_cm)
        weight_kg = float(weight_kg)
    except (ValueError, TypeError):
        return None, "Invalid data"

    if height_cm <= 0 or weight_kg <= 0:
        return None, "Invalid data"

    height_m = height_cm / 100
    bmi = weight_kg / (height_m**2)
    bmi = round(bmi, 1)

    # BMI category logic
    if bmi < 18.5:
        category = "Underweight"
    elif 18.5 <= bmi < 25:
        category = "Normal"
    elif 25 <= bmi < 30:
        category = "Overweight"
    else:
        category = "Obese"

    return bmi, category


@login_required(login_url="login")
def profile(request):
    user = request.user
    bmi_data = BodyMassIndex.objects.filter(user=user).first()

    if request.method == "POST":
        new_name = request.POST.get("fullName")
        new_email = request.POST.get("email")
        height = request.POST.get("height")
        weight = request.POST.get("weight")
        age = request.POST.get("age")
        gender = request.POST.get("gender")

        # Try casting inputs
        try:
            height_val = float(height)
            weight_val = float(weight)
            age_val = int(age)
        except (TypeError, ValueError):
            height_val = weight_val = age_val = None

        # Only update if all data is valid
        if height_val and weight_val and age_val and gender in ["M", "F", "O"]:
            bmi, category = calculate_bmi(height_val, weight_val)

            BodyMassIndex.objects.update_or_create(
                user=user,
                defaults={
                    "height": height_val,
                    "weight": weight_val,
                    "age": age_val,
                    "gender": gender,
                    "bmi": bmi,
                    "category": category,
                },
            )

            # Optional: use updated values for percent calc
            if bmi is not None:
                if bmi < 18.5:
                    bmi_percent = 10
                elif bmi < 25:
                    bmi_percent = 35
                elif bmi < 30:
                    bmi_percent = 65
                else:
                    bmi_percent = 90
            else:
                bmi_percent = 0
        else:
            bmi_percent = 0

        # Update user info
        CustomUser.objects.filter(id=user.id).update(
            full_name=new_name,
            email=new_email,
        )

        return redirect("profile")  # Refresh with updated data

    # Reload latest BMI data for GET or after POST redirect
    bmi_data = BodyMassIndex.objects.filter(user=user).first()
    bmi_percent = 0
    if bmi_data and bmi_data.bmi is not None:
        bmi = bmi_data.bmi
        if bmi < 18.5:
            bmi_percent = 10
        elif bmi < 25:
            bmi_percent = 35
        elif bmi < 30:
            bmi_percent = 65
        else:
            bmi_percent = 90

    context = {
        "name": user.full_name or "",
        "email": user.email or "",
        "height": bmi_data.height if bmi_data else None,
        "weight": bmi_data.weight if bmi_data else None,
        "age": bmi_data.age if bmi_data else None,
        "gender": bmi_data.gender if bmi_data else None,
        "bmi": bmi_data.bmi if bmi_data else None,
        "category": bmi_data.category if bmi_data else None,
        "bmi_percent": bmi_percent,
    }

    return render(request, "wellBite/profile.html", context)


@login_required(login_url="login")
def nutrition(request):
    return render(request, "wellBite/nutrition.html")
