import os
import django



# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from main_app.models import Astronaut, Mission, Spacecraft
from django.db.models import Q, Count, F


# from populate_db import populate_model_with_data


# # # Create queries within functions
# populate_model_with_data(Astronaut)
# populate_model_with_data(Spacecraft)
# populate_model_with_data(Mission)


def get_astronauts(search_string=None):
    if search_string is None:
        return ''
    astronauts = Astronaut.objects.filter(Q(name__icontains=search_string) | Q(phone_number__icontains=search_string)).order_by('name')

    if not astronauts.exists():
        return ''

    return '\n'.join(f"Astronaut: {a.name}, phone number: {a.phone_number}, status: {'Active' if a.is_active else 'Inactive'}" for a in astronauts)

def get_top_astronaut():

    if Mission.objects.count() == 0 or Astronaut.objects.count() == 0:
        return 'No data.'
    a = Astronaut.objects.annotate(num_missions=Count('missions')).order_by('-num_missions', 'phone_number').first()

    if not a or a.num_missions == 0:
        return 'No data.'

    return f"Top Astronaut: {a.name} with {a.missions.count()} missions."


def get_top_commander():

    if Mission.objects.count() == 0 or Mission.objects.filter(commander__isnull=False).count() == 0:
        return "No data."
    a = Astronaut.objects.annotate(commanded_missions_num=Count('commanded_missions')).order_by('-commanded_missions_num', 'phone_number').first()

    if not a:
        return "No data."

    return f"Top Commander: {a.name} with {a.commanded_missions_num} commanded missions."

def get_last_completed_mission():
    mission = Mission.objects.filter(status='Completed').order_by('-launch_date').first()

    if not mission:
        return 'No data.'

    if mission.commander is None:
        return 'TBA'

    return f"The last completed mission is: {mission.name}. Commander: {'TBA' if not mission.commander else mission.commander.name }. Astronauts: {', '.join(a.name for a in mission.astronauts.all().order_by('name'))}. Spacecraft: {mission.spacecraft.name}. Total spacewalks: {sum(a.spacewalks for a in mission.astronauts.all())}."


def get_most_used_spacecraft():
    spacecraft = Spacecraft.objects.annotate(num_missions=Count('missions'), num_astronauts=Count('missions__astronauts', distinct=True)).order_by('-num_missions', 'name').first()

    if Mission.objects.all() == 0:
        return 'No data.'

    return f"The most used spacecraft is: {spacecraft.name}, manufactured by {spacecraft.manufacturer}, used in {spacecraft.num_missions} missions, astronauts on missions: {spacecraft.num_astronauts}."


def decrease_spacecrafts_weight():
    spacecrafts = Spacecraft.objects.filter(missions__status='Planned').distinct().filter(weight__gte=200)

    if not spacecrafts.exists():
        return 'No changes in weight.'

    updated_spacecrafts = spacecrafts.update(weight = F('weight') - 200)

    return f"The weight of {updated_spacecrafts} spacecrafts has been decreased. The new average weight of all spacecrafts is {sum(s.weight for s in Spacecraft.objects.all()) / Spacecraft.objects.all().count():.1f}kg"


