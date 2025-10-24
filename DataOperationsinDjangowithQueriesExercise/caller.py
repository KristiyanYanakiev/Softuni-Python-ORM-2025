import os


import django


# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from main_app.models import Pet, Artifact, Location, Car
from django.db.models import QuerySet
from decimal import Decimal

from populate_db import populate_model_with_data
# Create queries within functions

def create_pet(name: str, species: str) -> str:
    pet = Pet.objects.create(name=name, species=species)
    return f"{pet.name} is a very cute {pet.species}!"

def create_artifact(name: str, origin: str, age: int, description: str, is_magical: bool) -> str:
    artifact = Artifact.objects.create(name=name, origin=origin, age=age, description=description, is_magical=is_magical)
    return f"The artifact {artifact.name} is {artifact.age} years old!"

def rename_artifact(artifact: Artifact, new_name: str) -> None:
    if artifact.age > 250 and artifact.is_magical:
        artifact.name = new_name
        artifact.save()

def delete_all_artifacts() -> None:
    Artifact.objects.all().delete()

def show_all_locations() -> str:
    populations = Location.objects.all().order_by("-id")

    return '\n'.join(f"{p.name} has a population of {p.population}!" for p in populations)


def new_capital() -> None:
    first_location = Location.objects.first()
    first_location.is_capital = True
    first_location.save()

def get_capitals() -> QuerySet:
    return Location.objects.filter(is_capital=True).values("name")


def delete_first_location() -> None:
    Location.objects.first().delete()

def apply_discount() -> None:
    cars_to_update = []
    for car in Car.objects.all():
        digits = car.year
        percentage_off = Decimal(str(sum(int(d) for d in str(digits) ) / 100))
        discount = car.price * percentage_off
        car.price_with_discount = car.price - discount
        cars_to_update.append(car)

    Car.objects.bulk_update(cars_to_update, ['price_with_discount'])

def get_recent_cars() -> QuerySet:
    return Car.objects.filter(year__gt=2020).values('model', 'price_with_discount')

def delete_last_car() -> None:
    Car.objects.last().delete()




