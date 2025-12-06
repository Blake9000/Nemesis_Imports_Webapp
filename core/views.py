# views.py
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import TemplateView, ListView
from .models import Car, CarImage

from .models import Car
from .forms import LoginForm, RegistrationForm, CarForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

def home(request):
    return render(request, "home.html")

def inventory(request):
    cars = Car.objects.filter(is_sold=False).order_by("-created_date")
    # derive unique makes for filter
    makes = sorted({c.make for c in cars})
    return render(request, "inventory.html", {"cars": cars, "makes": makes, "total_count": cars.count()})

def car_detail(request, pk):
    car = get_object_or_404(Car, pk=pk)
    return render(request, "admin/car_detail.html", {"car": car})

def about(request):
    return render(request, "about.html")

def contact(request):
    if request.method == "POST":
        # handle form submit later
        pass
    return render(request, "contact.html")

class AdminCars(LoginRequiredMixin,UserPassesTestMixin, ListView):
    template_name = "admin/admin_cars.html"
    model = Car
    context_object_name = "cars"

    def test_func(self):
        return self.request.user.is_superuser


def site_login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data["username"], password=form.cleaned_data["password"])
            if user is not None:
                login(request, user)
                return render(request, "partials/_log_in.html", {"form": LoginForm(), "success":True})
        else:
            messages.error(request, "Username or password is incorrect")
    return render(request, "partials/_log_in.html", {"form": LoginForm()})

def site_registration(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            login(request, new_user, backend="django.contrib.auth.backends.ModelBackend")
            return redirect("student-list-url")
    else:
        form = RegistrationForm()

    return render(request, "register.html", {"form": form})


def car_edit(request, pk):
    car = get_object_or_404(Car, pk=pk)

    if request.method == "POST":
        form = CarForm(request.POST, request.FILES, instance=car)
        if form.is_valid():
            car = form.save()

            for img in request.FILES.getlist("additional_images"):
                CarImage.objects.create(car=car, image=img)

            return redirect("admin_cars")
    else:
        form = CarForm(instance=car)

    return render(request, "admin/car_edit.html", {"form": form, "car": car})
def car_delete_confirm(request, pk):
    car = get_object_or_404(Car, pk=pk)
    # This returns only the modal content partial
    return render(request, "admin/partials/car_delete_confirm_modal.html", {"car": car})


def car_delete(request, pk):
    car = get_object_or_404(Car, pk=pk)

    if request.method == "POST":
        car.delete()

        if request.headers.get("HX-Request"):
            response = HttpResponse("", status=204)
            response["HX-Redirect"] = reverse("admin_cars")
            return response

        return redirect("admin_cars")

    # Non-POST fallback
    return redirect("admin_cars")

def car_create(request):
    if request.method == "POST":
        form = CarForm(request.POST, request.FILES)
        if form.is_valid():
            car = form.save()

            for img in request.FILES.getlist("additional_images"):
                CarImage.objects.create(car=car, image=img)

            return redirect("admin_cars")
    else:
        form = CarForm()

    return render(request, "admin/car_create.html", {"form": form})