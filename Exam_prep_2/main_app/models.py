from django.db import models

# Create your models here.
from django.db import models
from django.core.validators import MinLengthValidator, MaxLengthValidator, MinValueValidator, MaxValueValidator

from managers import DirectorModel


# Abstract base class for common person fields
class Person(models.Model):
    full_name = models.CharField(
        max_length=120,
        validators=[MinLengthValidator(2)]
    )
    birth_date = models.DateField(default='1900-01-01')
    nationality = models.CharField(
        max_length=50,
        default='Unknown'
    )

    class Meta:
        abstract = True


class Director(Person):
    years_of_experience = models.SmallIntegerField(
        default=0,
        validators=[MinValueValidator(0)]
    )

    def __str__(self):
        return self.full_name

    objects = DirectorModel()


class Actor(Person):
    is_awarded = models.BooleanField(default=False)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.full_name


class Movie(models.Model):
    GENRE_CHOICES = [
        ('Action', 'Action'),
        ('Comedy', 'Comedy'),
        ('Drama', 'Drama'),
        ('Other', 'Other')
    ]

    title = models.CharField(
        max_length=150,
        validators=[MinLengthValidator(5)]
    )
    release_date = models.DateField()
    storyline = models.TextField(null=True, blank=True)
    genre = models.CharField(
        max_length=6,
        choices=GENRE_CHOICES,
        default='Other'
    )
    rating = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        default=0.0,
        validators=[MinValueValidator(0.0), MaxValueValidator(10.0)]
    )
    is_classic = models.BooleanField(default=False)
    is_awarded = models.BooleanField(default=False)
    last_updated = models.DateTimeField(auto_now=True)

    director = models.ForeignKey(
        Director,
        on_delete=models.CASCADE
    )
    starring_actor = models.ForeignKey(
        Actor,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='starring_movies'
    )
    actors = models.ManyToManyField(
        Actor,
        related_name='movies'
    )

    def __str__(self):
        return self.title
