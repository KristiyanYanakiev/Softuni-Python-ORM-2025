from django.db import models


class RoomTypeChoices(models.TextChoices):
    Standard = 'Standard', 'Standard',
    Deluxe = 'Deluxe', 'Deluxe',
    Suite = 'Suite', 'Suite'

