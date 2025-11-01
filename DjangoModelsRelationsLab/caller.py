import os
import django



# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

from main_app.models import Lecturer, LecturerProfile

# Keep the data from the previous exercises, so you can reuse it
