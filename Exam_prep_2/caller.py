import os
import django


# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

from main_app.models import Director, Actor, Movie
from populate_db import populate_model_with_data
from django.db.models import Q, Count, Avg, F, Case, When, FloatField


# Import your models here

# Create queries within functions
def populate_db():
    populate_model_with_data(Director)
    populate_model_with_data(Actor)
    populate_model_with_data(Movie)

def get_directors(search_name=None, search_nationality=None):
    if search_name is  None and search_nationality is  None:
        return ''

    directors = Director.objects.filter(full_name__icontains=search_name, nationality__icontains=search_nationality).order_by('full_name')

    if not directors.exists():
        if search_name is not None:
            directors = Director.objects.filter(full_name__icontains=search_name).order_by('full_name')

        if search_nationality is not None:
            directors = Director.objects.filter(nationality__icontains=search_nationality).order_by('full_name')

        if not directors.exists():
            return ''

    return ''.join(f"Director: {d.full_name}, nationality: {d.nationality}, experience: {d.years_of_experience1}"for d in directors)


def get_top_director():
    d = Director.objects.get_directors_by_movies_count().first()

    if not d:
        return ''
    return f"Top Director: {d.full_name}, movies: {d.movies_count}."


def get_top_actor():
    a = Actor.objects.annotate(movies_count=Count('movies')).order_by('-movies_count', 'full_name').first()

    if not a or not a.movies.all().exists():
        return ''

    return f"Top Actor: {a.full_name}, starring in movies: {', '.join(m.title for m in a.movies.all())}, movies average rating: {a.movies.aggregate(avg=Avg('rating'))['avg']:.1f}"

def get_actors_by_movies_count():
    actors = Actor.objects.annotate(num_movies=Count('movies')).order_by('-num_movies', 'full_name')[:3]

    actors_with_movies = [a for a in actors if a.movies.exists()]

    if not actors_with_movies:
        return ''
    return ''.join(f"{a.full_name}, participated in {a.num_movies} movies" for a in actors_with_movies)


def get_top_rated_awarded_movie():
    m = Movie.objects.filter(is_awarded=True).order_by('-rating', 'title').first()
    if not m:
        return ''
    return f"Top rated awarded movie: {m.title}, rating: {m.rating}. Starring actor: {m.starring_actor if m.starring_actor else 'N/A'}. Cast: {', '.join(a.full_name for a in m.actors.all().order_by('full_name'))}."


def increase_rating():
    classic_movies = Movie.objects.filter(is_classic=True, rating__lt=10.0)

    if not classic_movies.exists():
        return "No ratings increased."

    classic_movies.update(
        rating=Case(
            When(rating__lte=9.9, then=F('rating') + 0.1),
            default=F('rating'),
            output_field=FloatField()
        )
    )

    return f"Rating increased for {classic_movies} movies."

