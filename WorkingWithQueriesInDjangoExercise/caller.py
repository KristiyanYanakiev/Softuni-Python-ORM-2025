import os


import django

from choices import LaptopBrandChoices, LaptopOperationSystemChoices

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

from main_app.models import ArtworkGallery, Laptop
from django.db.models import Case, When, Value
from typing import List


# Import your models
# Create and check models
# Run and print your queries

def show_highest_rated_art() -> str:
    res = ArtworkGallery.objects.all().order_by('-rating', 'id').first()
    return f"{res.art_name} is the highest-rated art with a {res.rating} rating!"

def bulk_create_arts(first_art: ArtworkGallery, second_art: ArtworkGallery) -> None:
    ArtworkGallery.objects.bulk_create([first_art, second_art])

def delete_negative_rated_arts() -> None:
    ArtworkGallery.objects.filter(rating__lt=0).delete()

def show_the_most_expensive_laptop() -> str:
    res = Laptop.objects.order_by('-price', '-id').first()
    return f"{res.brand} is the most expensive laptop available for {res.price}$!"

def bulk_create_laptops(args: List[Laptop]) -> None:
    Laptop.objects.bulk_create(args)

def update_to_512_GB_storage() -> None:
    Laptop.objects.filter(brand__in=[LaptopBrandChoices.ASUS, LaptopBrandChoices.LENOVO]).update(memory=512)

def update_to_16_GB_memory() -> None:
    Laptop.objects.filter(brand__in=[LaptopBrandChoices.APPLE, LaptopBrandChoices.DELL, LaptopBrandChoices.ACER]).update(memory=16)

def update_operation_systems() -> None:
    Laptop.objects.update(
        operation_system=Case(
            When(brand=LaptopBrandChoices.ASUS, then=Value(LaptopOperationSystemChoices.WINDOWS)),
            When(brand=LaptopBrandChoices.APPLE, then=Value(LaptopOperationSystemChoices.MACOS)),
            When(brand__in=[LaptopBrandChoices.DELL, LaptopBrandChoices.ACER], then=Value(LaptopOperationSystemChoices.LINUX)),
            When(brand=LaptopBrandChoices.LENOVO, then=Value(LaptopOperationSystemChoices.CHROMEOS))
        )
    )

def delete_inexpensive_laptops() -> None:
    Laptop.objects.filter(price__lt=1200).delete()

