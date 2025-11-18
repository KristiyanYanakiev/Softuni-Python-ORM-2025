from django.db import models
from django.db.models import Count


class DirectorModel(models.Manager):
    def get_directors_by_movies_count(self):
        return self.annotate(movies_count=Count('movie')).order_by('-movies_count', 'full_name')