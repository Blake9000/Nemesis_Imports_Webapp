# urls.py
from django.contrib.auth.views import LogoutView
from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("inventory/", views.inventory, name="inventory"),
    path("cars/<int:pk>/", views.car_detail, name="car_detail"),
    path("about/", views.about, name="about"),
    path("contact/", views.contact, name="contact"),
    path('login/', views.site_login, name='login'),
    path('register/', views.site_registration, name='register'),

    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),
]

