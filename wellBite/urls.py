from django.urls import path
from .views import *

urlpatterns = [
    path("", index, name="index"),
    path("choose/", choose, name="choose"),
    path("get_university/", get_university, name="get_university"),
    path("about/", about, name="about"),
    path("profile/", profile, name="profile"),
    path("show/", nutrition_menu, name="show"),
]
