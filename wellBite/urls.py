from django.urls import path
from .views import *

urlpatterns = [
    path("", index, name="index"),
    path("choose/", choose, name="choose"),
]
