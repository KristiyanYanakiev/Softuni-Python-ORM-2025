import os


import django
from django.db.models import QuerySet

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

from main_app.models import Book, Author, Artist, Song, Product, Review, Driver, DrivingLicense, Owner, Registration, \
    Car
from datetime import timedelta, date, datetime
from typing import List


# Create queries within functions
def show_all_authors_with_their_books() -> str:
    res = ''
    for author in Author.objects.all().order_by('-id'):
        if author.book_set.all():
            res += f'{author.name} has written - {", ".join(b.title for b in author.book_set.all())}!\n'

    return res[:-1]

def delete_all_authors_without_books() -> None:
    for a in Author.objects.all():
        if not a.book_set.all():
            a.delete()

def add_song_to_artist(artist_name: str, song_title: str) -> None:
    artist = Artist.objects.get(name=artist_name)
    song = Song.objects.get(title=song_title)
    artist.songs.add(song)

def get_songs_by_artist(artist_name: str) -> QuerySet:
    return Artist.objects.get(name=artist_name).songs.all().order_by('-id')

def remove_song_from_artist(artist_name: str, song_title: str) -> None:
    artist = Artist.objects.get(name=artist_name)
    song = Song.objects.get(title=song_title)
    artist.songs.remove(song)

def calculate_average_rating_for_product_by_name(product_name: str) -> float:
    product = Product.objects.get(name=product_name)

    return sum(r.rating for r in product.reviews.all()) / len(product.reviews.all())

def get_reviews_with_high_ratings(threshold: int) -> QuerySet[Review]:
    return Review.objects.filter(rating__gte=threshold)

def get_products_with_no_reviews() -> QuerySet[Product]:
    return Product.objects.filter(reviews__isnull=True).order_by('-name')

def delete_products_without_reviews() -> None:
    Product.objects.filter(reviews__isnull=True).delete()

def calculate_licenses_expiration_dates() -> str:
    return '\n'.join(
        f"License with number: {l.license_number} expires on {l.issue_date + timedelta(days=365)}!"
        for l in DrivingLicense.objects.all().order_by('-license_number')
    )

def get_drivers_with_expired_licenses(due_date: date):
    res = []
    for d  in Driver.objects.all():
        expiration_date = d.licence.issue_date + timedelta(days=365)
        if expiration_date < due_date:
            res.append(d)

    return res

def register_car_by_owner(owner: Owner) -> str:
    registration = Registration.objects.filter(car__isnull=True).first()
    car = Car.objects.filter(registration__isnull=True).first()

    car.registration = registration
    car.owner = owner
    registration.registration_date = datetime.today()
    car.save()
    registration.save()

    return f"Successfully registered {car.model} to {car.owner.name} with registration number {car.registration.registration_number}."

