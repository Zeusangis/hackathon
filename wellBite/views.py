from django.shortcuts import render
import requests
from django.contrib.auth.decorators import login_required


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

    return render(request, "wellBite/choose.html", {"universities": universities})
