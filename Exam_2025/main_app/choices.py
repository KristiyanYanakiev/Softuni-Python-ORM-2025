from django.db import models


class BookGenreChoices(models.TextChoices):
    FICTION = ('Fiction', 'Fiction')
    NON_FICTION = ('Non-Fiction', 'Non-Fiction')
    OTHER = ('Other', 'Other')

