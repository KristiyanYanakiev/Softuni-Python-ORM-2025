import os


import django

from choices import LaptopBrandChoices, LaptopOperationSystemChoices

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

from main_app.models import ArtworkGallery, Laptop, ChessPlayer, Meal, Dungeon
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

def bulk_create_chess_players(args: List[ChessPlayer]) -> None:
    ChessPlayer.objects.bulk_create(args)

def delete_chess_players() -> None:
    ChessPlayer.objects.filter(title__isnull=True).delete()

def change_chess_games_won() -> None:
    ChessPlayer.objects.filter(title='GM').update(games_won=30)

def change_chess_games_lost() -> None:
    ChessPlayer.objects.filter(title='no title').update(games_lost=25)

def change_chess_games_drawn() -> None:
    ChessPlayer.objects.all().update(games_drawn=10)

def grand_chess_title_GM() -> None:
    ChessPlayer.objects.filter(rating__gte=2400).update(title="GM")

def grand_chess_title_IM() -> None:
    ChessPlayer.objects.filter(rating__range=[2300, 2399]).update(title="IM")

def grand_chess_title_FM() -> None:
    ChessPlayer.objects.filter(rating__range=[2200, 2299 ]).update(title="FM")

def grand_chess_title_regular_player() -> None:
    ChessPlayer.objects.filter(rating__range=[0, 2199]).update(title='regular player')


def set_new_chefs() -> None:
    Meal.objects.update(
        chef=Case(
            When(type='Breakfast', then='Gordon Ramsay'),
            When(type='Lunch', then='Julia Child'),
            When(type='Dinner', then='Jamie Oliver'),
            When(type='Snack', then='Thomas Keller')
        )
    )

def set_new_preparation_times() -> None:
    Meal.objects.update(
        preparation_time=Case(
            When(type='Breakfast', then='10 minutes'),
            When(type='Lunch', then='12 minutes'),
            When(type='Dinner', then='15 minutes'),
            When(type='Snack', then='5 minutes')
        )
    )

def update_low_calorie_meals() -> None:
    Meal.objects.filter(meal_type__in=['Breakfast', 'Dinner']).update(calories=400)

def update_high_calorie_meals() -> None:
    Meal.objects.filter(meal_type__in=['Lunch', 'Snack']).update(calories=700)

def delete_lunch_and_snack_meals() -> None:
    Meal.objects.filter(meal_type__in=['Lunch', 'Snack']).delete()


def show_hard_dungeons() -> str:
    res = Dungeon.objects.filter(difficulty='Hard').order_by("-location")

    return '\n'.join(f"{d.name} is guarded by {d.boss_name} who has {d.boss_health} health points!" for d in res)

def bulk_create_dungeons(args: List[Dungeon]) -> None:
    Dungeon.objects.bulk_create(args)

def update_dungeon_names() -> None:
    Dungeon.objects.update(
        name=Case(
            When(difficulty='Easy', then=Value('The Erased Thombs')),
            When(difficulty='Medium', then=Value('The Coral Labyrinth')),
            When(difficulty='Hard', then=Value('The Lost Haunt'))
        )
    )

def update_dungeon_bosses_health() -> None:
    Dungeon.objects.exclude(difficulty="Easy").update(boss_health=500)

def update_dungeon_recommended_levels() -> None:
    Dungeon.objects.update(
        recommended_level=Case(
            When(difficulty='Easy', then=Value(25)),
            When(difficulty='Medium', then=Value(50)),
            When(difficulty='Hard', then=Value(75))
        )
    )

def update_dungeon_rewards() -> None:
    Dungeon.objects.update(
        reward=Case(
            When(boss_health=500, then=Value('1000 Gold')),
            When(location__startswith='E', then=Value('New dungeon unlocked')),
            When(location__endswith='s', then=Value('Dragonheart Amulet'))
        )
    )

def set_new_locations() -> None:
    Dungeon.objects.update(
        location = Case(
            When(recommended_level=25, then=Value('Enchanted Maze')),
            When(recommended_level=50, then=Value('Grimstone Mines')),
            When(recommended_level=75, then=Value('Shadowed Abyss'))
        )
    )


# Dungeon.objects.all().delete()


dungeon1 = Dungeon(
    name="Dungeon 1",
    boss_name="Boss 1",
    boss_health=1000,
    recommended_level=75,
    reward="Gold",
    location="Eternal Hell",
    difficulty="Hard",
)

dungeon2 = Dungeon(
    name="Dungeon 2",
    boss_name="Boss 2",
    boss_health=400,
    recommended_level=25,
    reward="Experience",
    location="Crystal Caverns",
    difficulty="Easy",
)



