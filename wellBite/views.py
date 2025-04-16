from django.shortcuts import render, redirect
import requests
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import google.generativeai as genai
import datetime
import json
from django.contrib import messages
import typing_extensions as typing
import os
import google.generativeai as genai
from google.generativeai import GenerativeModel
from typing import List
from typing_extensions import (
    TypedDict,
)  # Must use this for compatibility with Gemini schema
from typing_extensions import TypedDict
from typing import List, Literal
from user.models import CustomUser, BodyMassIndex
from dotenv import load_dotenv

load_dotenv()
gemini_api_key = os.getenv("GEMINI_API")

genai.configure(api_key=gemini_api_key)


food_names = {
    "Saturday": [
        "Grilled Black Bean Burger",
        "Crispy Chicken Sandwich",
        "Crispy Shoestring French Fries",
        "LIZ'S FRIED CHICKEN",
        "Grits (6 fl oz)",
        "Scrambled Eggs",
        "Bacon (2 slice)",
        "White Rice (1/2 cup)",
        "Roasted Butternut Squash",
        "Fresh Collard Greens",
        "Fried Egg",
        "Classic Cheese Pizza",
        "Pepperoni Pizza",
        "Spinach & Ricotta Pizza",
        "Biscuit",
        "Vanilla Iced Donut with Sprinkles",
        "White Dinner Roll",
        "Chocolate Chip Devil's Food Cake",
        "Chocolate Chip Cookie",
    ],
    "Sunday": [
        "Grilled Black Bean Burger",
        "Crispy Chicken Sandwich",
        "Crispy Shoestring French Fries",
        "LIZ'S FRIED CHICKEN",
        "Grits (6 fl oz)",
        "Scrambled Eggs",
        "Bacon (2 slice)",
        "White Rice (1/2 cup)",
        "Roasted Butternut Squash",
        "Fresh Collard Greens",
        "Fried Egg",
        "Classic Cheese Pizza",
        "Pepperoni Pizza",
        "Spinach & Ricotta Pizza",
        "Biscuit",
        "Vanilla Iced Donut with Sprinkles",
        "White Dinner Roll",
        "Chocolate Chip Devil's Food Cake",
        "Chocolate Chip Cookie",
    ],
    "Monday": [
        "Grits (6 fl oz)",
        "Scrambled Eggs",
        "Hash Brown Potatoes",
        "Bacon (2 slice)",
        "Fried Egg",
        "Cinnamon-Honey Granola",
        "Chocolate Donut Bites",
        "French Toast Sticks",
        "Cinnamon Roll",
    ],
    "Tuesday": [
        "Biscuit",
        "Cranberry Orange Scone",
        "Cinnamon-Sugar Donut",
    ],
    "Wednesday": [
        "Grits (6 fl oz)",
        "Scrambled Eggs",
        "O'Brien Potatoes",
        "Pork Sausage Patty",
        "Fried Egg",
        "Cinnamon-Honey Granola",
        "Biscuit",
        "Cranberry-Peach Mini Muffin",
        "Cinnamon Roll",
    ],
    "Thursday": [
        "Grits (6 fl oz)",
        "Scrambled Eggs",
        "Crispy Tater Tots",
        "Smoked Maple Sausage",
        "Fried Egg",
        "Cinnamon-Honey Granola",
        "Double Chocolate Chip Mini Muffin",
        "Vanilla Iced Donut with Sprinkles",
        "Waffles & Gravy",
    ],
    "Friday": [
        "Grits (6 fl oz)",
        "Scrambled Eggs",
        "O'Brien Potatoes",
        "Pork Sausage Patty",
        "Ham, Egg & Cheese Bagel",
        "Cinnamon-Honey Granola",
        "Biscuit",
        "Cherry-Topped Cinnamon Roll",
        "Marshmallow Donut",
    ],
}


<<<<<<< HEAD
=======

>>>>>>> 5a88b56ce5e357e069ac63942110c15dfe688dca
@login_required(login_url="login")
def index(request):
    return render(request, "wellBite/index.html")


@login_required(login_url="login")
def choose(request):
    bmi_data = BodyMassIndex.objects.filter(user=request.user).first()
    if not bmi_data:
        messages.warning(request, "Please fill out your profile first.")
        return redirect(
            "profile",
        )
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


@login_required(login_url="login")
def get_university(request):
    university_api = "http://universities.hipolabs.com"
    q = request.GET.get("query")
    universities = []

    if q:
        response = requests.get(f"{university_api}/search?name={q}")
        if response.status_code == 200:
            universities = response.json()

    return JsonResponse(universities, safe=False)


@login_required(login_url="login")
def about(request):
    return render(request, "wellBite/about.html")


def calculate_bmi(height_cm, weight_kg):

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
            messages.success(
                request,
                "Profile updated successfully.",
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


upsplash = os.getenv("UNSPLASH")


<<<<<<< HEAD
def image(food_item: str) -> str:
    ACCESS_KEY = upsplash
    url = "https://api.unsplash.com/search/photos"
    params = {"query": food_item, "client_id": ACCESS_KEY, "content_filter": "high"}
=======

>>>>>>> 5a88b56ce5e357e069ac63942110c15dfe688dca

import requests

PEXELS_API_KEY = "82KAJg1R36cqr87TBcuySuXBt2EXNSHY5rJhRhE4uLPCL8G6eMnTiuGq"
PEXELS_BASE_URL = "https://api.pexels.com/v1/search"

def image(query):
    headers = {
        "Authorization": PEXELS_API_KEY
    }
    params = {
        "query": query+" Food",
        "per_page": 1  # Need at least 2 images
    }
    
    response = requests.get(PEXELS_BASE_URL, headers=headers, params=params)
    
    if response.status_code == 200:
        data = response.json()
        photos = data.get("photos", [])
        
        return photos[0]["src"]["original"]
     
    else:
        return f"Error {response.status_code}: {response.text}"

# Example usage




# def image(food_item: str) -> str:
#     ACCESS_KEY = upsplash
#     url = "https://api.unsplash.com/search/photos"
#     params = {"query": food_item,"client_id": ACCESS_KEY,"content_filter": "high" }

#     response = requests.get(url, params=params)

#     if response.status_code == 200:
#         data = response.json()
#         if data["results"]:
#             return data["results"][0]["urls"]["regular"]
#         else:
#             return "https://example.com/default-food.jpg"  # fallback if no result
#     else:
#         print("Failed to fetch images:", response.status_code)
#         return "https://example.com/error-image.jpg"  # fallback for errors


class NutritionFacts(TypedDict, total=False):
    serving_size: str
    calories: float
    total_fat: float
    saturated_fat: float
    trans_fat: float
    cholesterol: float
    sodium: float
    total_carbohydrates: float
    dietary_fiber: float
    total_sugars: float
    added_sugars: float
    protein: float


class FoodItem(TypedDict):
    name: str
    calories: float
    type: str  # e.g., "protein", "carbohydrate"
    nutrition_facts: NutritionFacts  # ← added detailed breakdown
<<<<<<< HEAD
    category: str
=======

>>>>>>> 5a88b56ce5e357e069ac63942110c15dfe688dca


class Meal(TypedDict):
    meal_type: Literal["breakfast", "lunch", "dinner"]
    total_calories: float
    items: List[FoodItem]


class NutritionResponse(TypedDict):
    date: str  # Format: YYYY-MM-DD
    meals: List[Meal]
    daily_total_calories: float


#  tools='google_search_retrieval'

# Initialize the Gemini model with schema support
model = GenerativeModel(
    "gemini-1.5-flash",
    generation_config={
        "response_mime_type": "application/json",
        "response_schema": NutritionResponse,
    },
)
# model_text = GenerativeModel("gemini-1.5-flash")
# def image_search(food):
#     prompt=f"Generate a short one or two word small short food name so that it can be good for image search. The food name is {food}."
#     response = model_text.generate_content(prompt)
#     print(response.text)
#     return response.text


# Base prompt for the model


def main_ulm(
    diet: str, target: int, height: float, weight: float, bmi: float
) -> NutritionResponse:
    today = datetime.date.today()

    # Get day name (e.g., "Monday", "Tuesday", etc.)
    day_name = today.strftime("%A")
    items = food_names[day_name]
    base_prompt = f"""
You are a certified nutritionist. Accoding to items available  in menu i provided here {items} , generate a structured daily meal plan that meets the following criteria:
Also Note one two or three worded food name so it can be good for image search.
- **Calorie Target:** The entire day's meals should sum up to {target} calories.
- **User Details:** 
  - Height: {height} ( in inches )
  - Weight: {weight} ( in kilograms)
  - BMI: {bmi}
- **Meal Structure:** 
  - 3 main meals: breakfast, lunch, and dinner.
- **Meal Details:** 
  - List food items for each meal along with their respective calorie values.
  - Categorize each food item by its nutrient type (e.g., protein, carbohydrate, fat, etc.).
  - Provide a subtotal of calories per meal.
- **Output Format:** 
  - The output must be valid JSON that strictly conforms to the provided JSON schema.
  - Do not include any brackets, personal comments, or extraneous text outside of the JSON structure.
- Also make sure you provide different meals for breakfast lunch dinner and dont repeat meal
Follow these instructions carefully to create a precise, valid JSON response.
Make sure that you validate all the information from the universitie's dining menu.

"""

    new_prompt = f"{base_prompt} Make a tailored diet plan for the '{diet}' diet plan."
    response = model.generate_content(new_prompt)
    response_json = json.loads(response.text)

    try:
        # Gemini may return `response.text` or `response.parts[0].text`
        raw_json = (
            response.text if hasattr(response, "text") else response.parts[0].text
        )
        data = json.loads(raw_json)
    except Exception as e:
        print("Error parsing JSON:", e)
        return {}
    for meals in data["meals"]:
        for meal in meals["items"]:
            meal["image"] = image(meal["name"])
    data["date"] = datetime.date.today().strftime("%Y-%m-%d")

    return data


def main(
    diet: str, uni: str, target: int, height: float, weight: float, bmi: float
) -> NutritionResponse:
    base_prompt = f"""
You are a certified nutritionist. Accoding to tomrrow's menu  available on the {uni} Dining menu, generate a structured daily meal plan that meets the following criteria:
Also Note one two or three worded food name so it can be good for image search descriptive 
- **Calorie Target:** The entire day's meals should sum up to {target} calories.
- **User Details:** 
  - Height: {height} ( in inches )
  - Weight: {weight} ( in kilograms)
  - BMI: {bmi}
- **Meal Structure:** 
  - 3 main meals: breakfast, lunch, and dinner.
- **Meal Details:** 
  - List food items for each meal along with their respective calorie values.
  - Categorize each food item by its nutrient type (e.g., protein, carbohydrate, fat, etc.).
  - Provide a subtotal of calories per meal.
- **Output Format:** 
  - The output must be valid JSON that strictly conforms to the provided JSON schema.
  - Do not include any brackets, personal comments, or extraneous text outside of the JSON structure.
- Also make sure you provide different meals for breakfast lunch dinner and dont repeat meal
Follow these instructions carefully to create a precise, valid JSON response.
Make sure that you validate all the information from the universitie's dining menu.

"""

    new_prompt = f"{base_prompt} Make a tailored diet plan for the '{diet}' diet plan."
    response = model.generate_content(new_prompt)
    response_json = json.loads(response.text)

    try:
        # Gemini may return `response.text` or `response.parts[0].text`
        raw_json = (
            response.text if hasattr(response, "text") else response.parts[0].text
        )
        data = json.loads(raw_json)
    except Exception as e:
        print("Error parsing JSON:", e)
        return {}
    for meals in data["meals"]:
        for meal in meals["items"]:
            meal["image"] = image(meal["name"])
    data["date"] = datetime.date.today().strftime("%Y-%m-%d")

    return data


def nutrition_menu(request):
    user = request.user
    bmi_data = BodyMassIndex.objects.filter(user=user).first()
    if not bmi_data:
        messages.warning(request, "Please fill out your profile first.")
        return redirect(
            "profile",
        )
    height = bmi_data.height
    weight = bmi_data.weight
    bmi = bmi_data.bmi
    if request.method == "POST":
        print("POST")
        university = request.POST.get("university_name")
        selected_plan = request.POST.get("selected_options")
        diet = request.POST.get("meal_plan")
        print(university)
        if university == "University of Louisiana at Monroe":
            print("GO")
            meal_plan = main_ulm(selected_plan, diet, height, weight, bmi)
        else:
            print("Ready")
            meal_plan = main(university, selected_plan, diet, height, weight, bmi)
    context = {
        "daily_menu": meal_plan,
    }
    return render(request, "wellBite/show.html", context=context)
