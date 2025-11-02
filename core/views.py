# views.py
from django.shortcuts import render, get_object_or_404
#from .models import Car  # adapt to your app

def home(request):
    return render(request, "home.html")
'''
def inventory(request):
    cars = Car.objects.filter(is_sold=False).order_by("-created_date")
    # derive unique makes for filter
    makes = sorted({c.make for c in cars})
    return render(request, "inventory.html", {"cars": cars, "makes": makes, "total_count": cars.count()})

def car_detail(request, pk):
    car = get_object_or_404(Car, pk=pk)
    return render(request, "car_detail.html", {"car": car})
'''
def about(request):
    return render(request, "about.html")
'''
def contact(request):
    if request.method == "POST":
        # handle form submit later
        pass
    return render(request, "contact.html")
'''