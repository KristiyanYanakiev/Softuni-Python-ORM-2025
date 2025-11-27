from django.db import models
from django.db.models import Count


class HouseCustomManager(models.Manager):
    def get_houses_by_dragons_count(self):
        return self.annotate(num_of_dragons=Count('dragon')).order_by('-num_of_dragons', 'name')