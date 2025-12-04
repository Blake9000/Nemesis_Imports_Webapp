# views.py
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from .models import Car
from .forms import LoginForm

def home(request):
    return render(request, "home.html")

def inventory(request):
    cars = Car.objects.filter(is_sold=False).order_by("-created_date")
    # derive unique makes for filter
    makes = sorted({c.make for c in cars})
    return render(request, "inventory.html", {"cars": cars, "makes": makes, "total_count": cars.count()})

def car_detail(request, pk):
    car = get_object_or_404(Car, pk=pk)
    return render(request, "car_detail.html", {"car": car})

def about(request):
    return render(request, "about.html")

def contact(request):
    if request.method == "POST":
        # handle form submit later
        pass
    return render(request, "contact.html")

def site_login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data["username"], password=form.cleaned_data["password"])
            if user is not None:
                login(request, user)
            return redirect('about')
        else:
            messages.error(request, "Username or password is incorrect")
    return render(request, "partials/_log_in.html", {"form": LoginForm()})

def site_registration(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            login(request, new_user)
            return redirect("student-list-url")
    else:
        form = StudentSignUpForm()

    return render(request, "students/signup.html", {"form": form})