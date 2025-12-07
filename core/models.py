from django.db import models
import os
from datetime import datetime

def timestamped_image_path(instance, filename):
    base, ext = os.path.splitext(filename)
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    new_name = f"{base}-{timestamp}{ext}"
    return f"car_photos/{new_name}"


class Car(models.Model):
    TRANSMISSION_CHOICES = (
        ("MANUAL", "Manual"),
        ("AUTOMATIC", "Automatic"),
    )
    CONDITION_CHOICES = (
        ("POOR", "Poor"),
        ("BELOW_AVERAGE", "Below Average"),
        ("GOOD", "Good"),
        ("VERY_GOOD", "Very Good"),
        ("EXCELLENT", "Excellent"),
        ("UNKNOWN", "Unknown"),
    )

    make = models.CharField(max_length=128)
    model = models.CharField(max_length=128)
    year = models.IntegerField()
    engine = models.CharField(max_length=128, blank=True, null=True)
    transmission = models.CharField(
        max_length=128,
        choices=TRANSMISSION_CHOICES,
        default="MANUAL",
    )
    mileage = models.IntegerField(blank=True, null=True)
    price = models.FloatField(blank=True, null=True)
    color = models.CharField(max_length=50, blank=True, null=True)
    condition = models.CharField(
        max_length=50,
        choices=CONDITION_CHOICES,
        default="UNKNOWN",
    )
    description = models.TextField(blank=True, null=True)
    additional_features = models.JSONField(default=list, blank=True)
    primary_image = models.ImageField(
        upload_to=timestamped_image_path,
        blank=True,
        null=True,
    )
    is_featured = models.BooleanField(default=False)
    is_sold = models.BooleanField(default=False)
    import_date = models.DateTimeField(auto_now_add=False)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.year} {self.make} {self.model}"
    def delete(self, *args, **kwargs):
        # Delete primary image file if present
        if self.primary_image:
            self.primary_image.delete(save=False)

        for extra in self.extra_images.all():
            extra.delete()

        super().delete(*args, **kwargs)


class CarImage(models.Model):
    car = models.ForeignKey(
        Car,
        on_delete=models.CASCADE,
        related_name="extra_images",
    )
    image = models.ImageField(upload_to=timestamped_image_path)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image for {self.car}"

    def delete(self, *args, **kwargs):
        if self.image:
            self.image.delete(save=False)
        super().delete(*args, **kwargs)