# setup

import google.generativeai as genai
from google.colab import userdata



import json
import dataclasses
import typing_extensions as typing
import os


genai.configure(api_key="AIzaSyDrP2GybosJJtb4J62o13r_c5_Ka0qS3H8")

import google.generativeai as genai
from google.generativeai import GenerativeModel

from typing import List
from typing_extensions import TypedDict  # Must use this for compatibility with Gemini schema





from typing_extensions import TypedDict
from typing import List, Literal


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


class Meal(TypedDict):
    meal_type: Literal["breakfast", "lunch", "dinner"]
    total_calories: float
    items: List[FoodItem]


class NutritionResponse(TypedDict):
    date: str  # Format: YYYY-MM-DD
    meals: List[Meal]
    daily_total_calories: float




# Initialize the Gemini model with schema support
model = GenerativeModel(
   'gemini-1.5-flash',
    generation_config={
        "response_mime_type": "application/json",
        "response_schema": NutritionResponse
    }
)

# Base prompt for the model



def main(diet: str, uni: str, target: int, height: float, weight: float) -> NutritionResponse:
    base_prompt = (
        f"""
You are a certified nutritionist. Using only the food items available on the {uni} Dining menu, generate a structured daily meal plan that meets the following criteria:

- **Calorie Target:** The entire day's meals should sum up to {target} calories.
- **User Details:** 
  - Height: {height} ( in inches )
  - Weight: {weight} ( in kilograms)
- **Meal Structure:** 
  - 3 main meals: breakfast, lunch, and dinner.
- **Meal Details:** 
  - List food items for each meal along with their respective calorie values.
  - Categorize each food item by its nutrient type (e.g., protein, carbohydrate, fat, etc.).
  - Provide a subtotal of calories per meal.
- **Output Format:** 
  - The output must be valid JSON that strictly conforms to the provided JSON schema.
  - Do not include any brackets, personal comments, or extraneous text outside of the JSON structure.

Follow these instructions carefully to create a precise, valid JSON response.
"""
    )


    new_prompt = f"{base_prompt} Make a tailored diet plan for the '{diet}' diet plan."
    response = model.generate_content(new_prompt)
    response_json = json.loads(response.text)


    try:
        # Gemini may return `response.text` or `response.parts[0].text`
        raw_json = response.text if hasattr(response, 'text') else response.parts[0].text
        data = json.loads(raw_json)
    except Exception as e:
        print("Error parsing JSON:", e)
        return {}
    for meals in data["meals"]:
      for meal in meals["items"]:
        meal["image"] = image(meal["name"])
    return data
  # or `response` depending on whether you want raw object or text






# Guide use this function based on such parameter
# !pip -q install google-generativeai newspaper3k
# The data uses inches and kg
# data=main(diet="Lactose Intolorant",uni="ULM",height=72,weight=60)



