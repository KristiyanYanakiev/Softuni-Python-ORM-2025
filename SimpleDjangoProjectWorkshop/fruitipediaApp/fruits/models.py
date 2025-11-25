
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.db import models
from django.template.context_processors import request


# Create your models here.
class Category(models.Model):
    name = models.CharField(
        unique=True,
        max_length=100
    )


class Fruit(models.Model):
    name = models.CharField(
        validators=[MinLengthValidator(2), MaxLengthValidator(30)],
        max_length=100
    )
    Image_url = models.URLField()
    description = models.TextField()
    nutrition = models.TextField(null=True, blank=True)
