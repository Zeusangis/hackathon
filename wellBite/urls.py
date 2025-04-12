from django.urls import path
from .views import *

urlpatterns = [
    path("", index, name="index"),
    path("choose/", choose, name="choose"),
    path("get_university/", get_university, name="get_university"),
    path("submit_choices/", submit_choices, name="submit_choices"),
]
