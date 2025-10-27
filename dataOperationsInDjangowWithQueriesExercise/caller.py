import os


import django

from main_app.RoomTypeChoices import RoomTypeChoices

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from main_app.models import Pet, Artifact, Location, Car, Task, HotelRoom
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


def show_unfinished_tasks() -> str:
    return '\n'.join(
        f"Task - {t.title} needs to be done until {t.due_date}!"
        for t in Task.objects.filter(is_finished=False)
    )

def complete_odd_tasks() -> None:
    updated_tasks = []
    for t in Task.objects.all():
        if t.id % 2 != 0:
            t.is_finished = True
            updated_tasks.append(t)
    Task.objects.bulk_update(updated_tasks, ["is_finished"])

def encode_and_replace(text: str, task_title: str) -> None:
    encoded_tasks = []
    encoded_text = ''.join(chr(ord(l) - 3) for l in text)

    for t in Task.objects.filter(title = task_title):
        t.description = encoded_text
        encoded_tasks.append(t)

    Task.objects.bulk_update(encoded_tasks, ['description'])

def get_deluxe_rooms() -> str:
    return "\n".join(f"Deluxe room with number {r.room_number} costs {r.price_per_night}$ per night!" for r in HotelRoom.objects.filter(room_type = RoomTypeChoices.Deluxe))

def increase_room_capacity() -> None:
    previous_room = None
    for r in HotelRoom.objects.filter(is_reserved=True).order_by("id"):
        if previous_room:
            r.capacity += previous_room.capacity
        else:
            r.capacity += r.id

        previous_room = r
        r.save()

def reserve_first_room() -> None:
    r = HotelRoom.objects.first()
    r.is_reserved = True
    r.save()

def delete_last_room() -> None:
    r = HotelRoom.objects.last()

    if not r.is_reserved:
        r.delete()




