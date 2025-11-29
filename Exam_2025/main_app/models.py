from django.core.validators import MinLengthValidator, MaxLengthValidator, MinValueValidator, MaxValueValidator
from django.db import models

from main_app.choices import BookGenreChoices
from main_app.managers import PublisherCustomManager


class NameCountryModel(models.Model):
    name = models.CharField(
        max_length=100,
        validators=[MinLengthValidator(3)]
    )

    country = models.CharField(
        max_length=40,
        default='TBC'
    )

    class Meta:
        abstract = True


class Publisher(NameCountryModel):

    established_date = models.DateField(
        default='1800-01-01'
    )

    rating = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(5.0)],
        default=0.0
    )

    def __str__(self):
        return self.name

    objects = PublisherCustomManager()

class Author(NameCountryModel):
    birth_date = models.DateField(
        null=True,
        blank=True
    )
    is_active = models.BooleanField(
        default=True
    )
    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(
        max_length=200,
        validators=[MinLengthValidator(2)]
    )
    publication_date = models.DateField()
    summary = models.TextField(
        null=True,
        blank=True
    )
    genre = models.CharField(
        choices=BookGenreChoices.choices,
        max_length=11,
        default=BookGenreChoices.OTHER
    )
    price = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        validators=[MinValueValidator(0.01), MaxValueValidator(9999.99)],
        default= 0.01
    )
    rating = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(5.0)],
        default=0.0
    )
    is_bestseller = models.BooleanField(
        default=False
    )
    updated_at = models.DateTimeField(
        auto_now=True
    )
    publisher = models.ForeignKey(
        to=Publisher,
        on_delete=models.CASCADE
    )
    main_author = models.ForeignKey(
        to=Author,
        on_delete=models.CASCADE,
        related_name='books'
    )

    co_authors = models.ManyToManyField(
        to=Author,
        related_name='co_authored_books'
    )

    def __str__(self):
        return self.title