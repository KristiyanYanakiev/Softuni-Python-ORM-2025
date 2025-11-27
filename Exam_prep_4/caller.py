import os
import django
from django.db.models import Q, F

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here

# Create queries within functions
from datetime import date, datetime
from main_app.models import House, Dragon, Quest

def get_houses(search_string=None):

    houses = House.objects.filter(
        Q(name__istartswith=search_string)
            |
        Q(motto__istartswith=search_string)
    )

    if not houses.exists() or search_string in [None, '']:
        return 'No houses match your search.'

    return '\n'.join(f"House: {h.name}, wins: {h.wins}, motto: {h.motto if h.motto else 'N/A'}" for h in houses)


def get_most_dangerous_house():
    h = House.objects.get_houses_by_dragons_count().first()

    if House.objects.all() == 0 or Dragon.objects.all() == 0:
        return 'No relevant data.'

    return f"The most dangerous house is the House of {h.name} with {h.dragon_set.count()} dragons. Currently {'rulling' if h.is_ruling else 'not ruling'} the kingdom."


def get_most_powerful_dragon():
    d = Dragon.objects.filter(is_healthy=True).order_by('-power', 'name').first()

    if not d:
        return 'No relevant data.'

    return f"The most powerful healthy dragon is {d.name} with a power level of {d.power}, breath type {d.breath}, and {d.wins} wins, coming from the house of {d.house.name}. Currently participating in {d.quest_set.count()} quests."


def update_dragons_data():
    dragons = Dragon.objects.filter(is_healthy=False, power__gt=1.0)

    num_of_dragons_affected = dragons.update(power=F('power') - 0.1, is_healthy=False)

    if num_of_dragons_affected == 0:
        return 'No changes in dragons data.'

    return f"The data for {num_of_dragons_affected} dragon/s has been changed. The minimum power level among all dragons is {min(d.power for d in dragons):.1f}"


def get_earliest_quest():
    q = Quest.objects.order_by('start_time').first()

    if Quest.objects.all() == 0:
        return 'No relevant data.'

    day = q.start_time.day
    month = q.start_time.month
    year = q.start_time.year
    avg_power_level = sum(d.power for d in q.dragons.all()) / len(q.dragons.all())

    return f"The earliest quest is: {q.name}, code: {q.code}, start date: {day}.{month}.{year}, host: {q.host.name}. Dragons: {'*'.join(d.name for d in q.dragons.all())}. Average dragons power level: {avg_power_level:.2f}"


def announce_quest_winner(quest_code):
    quest = Quest.objects.filter(code=quest_code).first()

    if not quest:
        return 'No such quest.'

    dragon = quest.dragons.order_by('-power', 'name').first()

    dragon.wins += 1
    dragon.wins += 1
    dragon.save()

    quest.delete()

    return f"The quest: {quest.name} has been won by dragon {dragon.name} from house { dragon.house.name}. The number of wins has been updated as follows: {dragon.wins} total wins for the dragon and {dragon.house.wins} total wins for the house. The house was awarded with {quest.reward:.2f} coins."


