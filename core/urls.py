# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("inventory/", views.inventory, name="inventory"),
    path("cars/<int:pk>/", views.car_detail, name="car_detail"),
    path("about/", views.about, name="about"),
    path("contact/", views.contact, name="contact"),

    path("management/", views.management, name="management"),
]

