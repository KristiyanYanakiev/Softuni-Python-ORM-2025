from django.core.validators import MinLengthValidator, MaxLengthValidator, MinValueValidator, MaxValueValidator, \
    RegexValidator
from django.db import models
from django.utils import timezone

from main_app.choices import BreadthChoices
from main_app.managers import HouseCustomManager


# Create your models here.
class House(models.Model):
    name = models.CharField(
        max_length=80,
        validators=[MinLengthValidator(5), MaxLengthValidator(80)],
        unique=True
    )
    motto = models.TextField(
        blank=True,
        null=True
    )
    is_ruling = models.BooleanField(default=False)
    castle = models.CharField(
        max_length=80,
        validators=[MaxLengthValidator(80)],
        null=True,
        blank=True
    )
    wins = models.PositiveSmallIntegerField(
        default=0
    )
    modified_at = models.DateTimeField(auto_now=True)

    objects = HouseCustomManager()

    def __str__(self):
        return self.name


class Dragon(models.Model):
    name = models.CharField(
        max_length=80,
        validators=[MinLengthValidator(5), MaxLengthValidator(80)],
        unique=True
    )
    power = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        validators=[MinValueValidator(1.0), MaxValueValidator(10.0)],
        default=1.0

    )

    breath = models.CharField(
        max_length=200,
        choices=BreadthChoices.choices,
        default=BreadthChoices.UNKNOWN
    )

    is_healthy = models.BooleanField(
        default=True
    )

    birth_date = models.DateField(
        default=timezone.now
    )

    wins = models.PositiveSmallIntegerField(
        default=0
    )

    modified_at = models.DateTimeField(
        auto_now=True
    )

    house = models.ForeignKey(
        to=House,
        on_delete=models.CASCADE
    )

class Quest(models.Model):
    name = models.CharField(
        max_length=80,
        validators=[MinLengthValidator(5), MaxLengthValidator(80)],
        unique=True
    )
    code = models.CharField(
        max_length=200,
        validators=[RegexValidator(
            regex=r'^[A-Za-z#]{4}$',
            message='Code must contain exactly 4 characters: letters (A–Z, a–z) or "#".'
        )],
        unique=True
    )

    reward = models.FloatField(
        default=100.0
    )
    start_time = models.DateTimeField()
    modified_at = models.DateTimeField(
        auto_now=True
    )
    dragons = models.ManyToManyField(Dragon)
    host = models.ForeignKey(to=House, on_delete=models.CASCADE)
