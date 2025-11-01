import os
import django
from django.db.models import QuerySet

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

from main_app.models import Book, Author, Artist, Song


# Create queries within functions
def show_all_authors_with_their_books() -> str:
    res = ''
    for author in Author.objects.all().order_by('-id'):
        if author.book_set.all():
            res += f'{author.name} has written - {", ".join(b.title for b in author.book_set.all())}!\n'

    return res[:-1]

def delete_all_authors_without_books() -> None:
    for a in Author.objects.all():
        if not a.book_set.all():
            a.delete()

def add_song_to_artist(artist_name: str, song_title: str) -> None:
    artist = Artist.objects.get(name=artist_name)
    song = Song.objects.get(title=song_title)
    artist.songs.add(song)

def get_songs_by_artist(artist_name: str) -> QuerySet:
    return Artist.objects.get(name=artist_name).songs.all().order_by('-id')

def remove_song_from_artist(artist_name: str, song_title: str) -> None:
    artist = Artist.objects.get(name=artist_name)
    song = Song.objects.get(title=song_title)
    artist.songs.remove(song)


