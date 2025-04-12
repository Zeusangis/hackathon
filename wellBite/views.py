from django.shortcuts import render
import requests


def index(request):
    return render(request, "wellBite/index.html")


def choose(request):
    university_api = "http://universities.hipolabs.com"
    universities = []

    if request.method == "POST":
        query = request.POST.get("query")
        if query:
            try:
                response = requests.get(f"{university_api}/search?name={query}")
                if response.status_code == 200:
                    universities = response.json()
            except requests.exceptions.RequestException as e:
                print(f"Error fetching data: {e}")
    else:
        # Default search if no query provided
        try:
            response = requests.get(f"{university_api}/search?name=university")
            if response.status_code == 200:
                universities = response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data: {e}")

    return render(request, "wellBite/choose.html", {"universities": universities})
