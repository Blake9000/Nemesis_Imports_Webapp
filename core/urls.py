# urls.py
from django.contrib.auth.views import LogoutView
from django.urls import path
from . import views
from .views import AdminCars

urlpatterns = [
    path("", views.home, name="home"),
    path("inventory/", views.inventory, name="inventory"),
    path("cars/<int:pk>/", views.car_detail, name="car_detail"),
    path("about/", views.about, name="about"),
    path("contact/", views.contact, name="contact"),
    path('login/', views.site_login, name='login'),
    path('register/', views.site_registration, name='register'),
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),

    path('admin_cars/', AdminCars.as_view(), name='admin_cars'),
    path("cars/<int:pk>/edit/", views.car_edit, name="car_edit"),
    path("cars/<int:pk>/delete/confirm/", views.car_delete_confirm, name="car_delete_confirm"),
    path("cars/<int:pk>/delete/", views.car_delete, name="car_delete"),
    path("cars/new/", views.car_create, name="car_create"),

]

