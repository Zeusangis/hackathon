from django.shortcuts import render

# import requests


def index(request):
    return render(request, "wellBite/index.html")


def choose(request):
    # university_api = "http://universities.hipolabs.com"
    # if request.method == "POST":
    #     query = request.POST.get("query")
    #     if query:
    #         response = requests.get(f"{university_api}/search?name={query}")
    #         universities = response.json()
    #         return render(
    #             request, "wellBite/choose.html", {"universities": universities}
    #         )
    return render(request, "wellBite/choose.html")
