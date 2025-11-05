import os
from tkinter.font import names

import django



# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from main_app.models import Animal, Mammal

# Create queries within functions
from main_app.models import ZooKeeper, Veterinarian

# Keep the data from the previous exercise, so you can reuse it

from main_app.models import ZooKeeper
