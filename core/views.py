# views.py
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import TemplateView, ListView
from .models import Car, CarImage

from .models import Car
from .forms import LoginForm, RegistrationForm, CarForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

def home(request):
    cars = Car.objects.filter(is_sold=False).filter(is_featured=True)
    return render(request, "home.html", {"cars": cars})
def inventory(request):
    # Base queryset: all cars in inventory
    cars_qs = Car.objects.all()

    # For the "of X total" text
    total_count = cars_qs.count()

    # Distinct makes for the dropdown
    makes = (
        Car.objects.values_list("make", flat=True)
        .distinct()
        .order_by("make")
    )

    # Get filter values from query string
    q = request.GET.get("q", "").strip()
    make = request.GET.get("make", "").strip()
    decade = request.GET.get("decade", "").strip()
    sort = request.GET.get("sort", "newest").strip()

    # Text search across make, model, year, and optionally description
    if q:
        cars_qs = cars_qs.filter(
            Q(make__icontains=q)
            | Q(model__icontains=q)
            | Q(year__icontains=q)
            | Q(description__icontains=q)
        )

    # Filter by make
    if make:
        cars_qs = cars_qs.filter(make=make)

    # Filter by decade: 1970 -> 1970 to 1979, etc
    if decade:
        try:
            start_year = int(decade)
            end_year = start_year + 9
            cars_qs = cars_qs.filter(year__gte=start_year, year__lte=end_year)
        except ValueError:
            pass  # ignore bad decade values

    # Sorting
    if sort == "price-low":
        cars_qs = cars_qs.order_by("price")
    elif sort == "price-high":
        cars_qs = cars_qs.order_by("-price")
    elif sort == "year-new":
        cars_qs = cars_qs.order_by("-year")
    elif sort == "year-old":
        cars_qs = cars_qs.order_by("year")
    else:
        # "newest" default - using id as a simple proxy for latest
        cars_qs = cars_qs.order_by("-id")

    # Pagination
    paginator = Paginator(cars_qs, 9)  # 9 cars per page
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "cars": page_obj.object_list,
        "page_obj": page_obj,
        "makes": makes,
        "total_count": total_count,
    }

    return render(request, "inventory.html", context)

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