from django.db import models

# Create your models here.
class Car(models.Model):
    TRANSMISSION_CHOICES = (
    ("MANUAL", "Manual"),
    ("AUTOMATIC", "Automatic")
    )
    CONDITION_CHOICES = (
    ("POOR", "Poor"),
    ("BELOW_AVERAGE", "Below Average"),
    ("GOOD", "Good"),
    ("VERY_GOOD", "Very Good"),
    ("EXCELLENT", "Excellent"),
    ("UNKNOWN", "Unknown")
    )
    make = models.CharField(max_length=128)
    model = models.CharField(max_length=128)
    year = models.IntegerField()
    engine = models.CharField(max_length=128, blank=True, null=True)
    transmission = models.CharField(max_length=128, choices=TRANSMISSION_CHOICES, default="MANUAL")
    mileage = models.IntegerField(blank=True, null=True)
    price = models.FloatField(blank=True, null=True)
    color = models.CharField(max_length=50, blank=True, null=True)
    condition = models.CharField(max_length=50, choices=CONDITION_CHOICES, default="UNKNOWN")
    description = models.TextField(blank=True, null=True)
    additional_features = models.JSONField(default=list, blank=True)
    is_featured = models.BooleanField(default=False)
    is_sold = models.BooleanField(default=False)
    import_date = models.DateTimeField(auto_now_add=False)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

class CarImage(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField()
    caption = models.TextField(max_length=200,blank=True, null=True)

    def __str__(self):
        return f"Image for {self.car.name}"