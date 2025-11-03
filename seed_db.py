import os
import django
from datetime import datetime

# Setup Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Nemesis_Imports.settings")
django.setup()

from core.models import Car, CarImage

cars_data = [
    {
        "make": "Toyota",
        "model": "Supra",
        "year": 1998,
        "engine": "3.0L I6 Turbo",
        "transmission": "MANUAL",
        "mileage": 65000,
        "price": 55000.00,
        "color": "Red",
        "condition": "EXCELLENT",
        "description": "Classic JDM icon with twin-turbo engine and 6-speed manual.",
        "additional_features": ["Targa Top", "Brembo Brakes", "Aftermarket Exhaust"],
        "is_featured": True,
        "is_sold": False,
        "import_date": datetime(2023, 8, 15),
        "images": [
            {"image": "car_images/supra_front.jpg", "caption": "Front view"},
            {"image": "car_images/supra_interior.jpg", "caption": "Interior"}
        ]
    },
    {
        "make": "Nissan",
        "model": "Skyline GT-R R34",
        "year": 1999,
        "engine": "2.6L RB26DETT",
        "transmission": "MANUAL",
        "mileage": 45000,
        "price": 89000.00,
        "color": "Bayside Blue",
        "condition": "VERY_GOOD",
        "description": "Imported R34 GT-R with full Nismo package and clean history.",
        "additional_features": ["AWD", "Boost Gauge", "Recaro Seats"],
        "is_featured": True,
        "is_sold": False,
        "import_date": datetime(2024, 3, 12),
        "images": [
            {"image": "car_images/r34_side.jpg", "caption": "Side profile"},
            {"image": "car_images/r34_engine.jpg", "caption": "RB26 engine bay"}
        ]
    },
    {
        "make": "Mazda",
        "model": "RX-7 FD3S",
        "year": 1993,
        "engine": "1.3L 13B-REW Twin Turbo Rotary",
        "transmission": "MANUAL",
        "mileage": 72000,
        "price": 43000.00,
        "color": "Yellow",
        "condition": "GOOD",
        "description": "Legendary lightweight rotary with upgraded cooling and suspension.",
        "additional_features": ["Tein Coilovers", "Front Lip", "RE-Amemiya Exhaust"],
        "is_featured": False,
        "is_sold": False,
        "import_date": datetime(2022, 11, 20),
        "images": [
            {"image": "car_images/rx7_front.jpg", "caption": "Front view"},
            {"image": "car_images/rx7_rear.jpg", "caption": "Rear angle"}
        ]
    }
]

for car_data in cars_data:
    images_data = car_data.pop("images", [])
    car = Car.objects.create(**car_data)
    for img in images_data:
        CarImage.objects.create(car=car, **img)
    print(f"Added: {car.make} {car.model} ({car.year})")

print("Database seeded successfully.")
