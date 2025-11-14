import os
import django



# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

from main_app.models import VideoGame
# Import your models here
# Create instances of VideoGame with real data
game1 = VideoGame.objects.create(
    title="The Last of Us Part II",
    genre="Action",
    release_year=2020,
    rating=9.0
)

game2 = VideoGame.objects.create(
    title="Cyberpunk 2077",
    genre="RPG",
    release_year=2020,
    rating=7.2
)

game3 = VideoGame.objects.create(
    title="Red Dead Redemption 2",
    genre="Adventure",
    release_year=2018,
    rating=9.7
)

game4 = VideoGame.objects.create(
    title="FIFA 22",
    genre="Sports",
    release_year=2021,
    rating=8.5
)

game5 = VideoGame.objects.create(
    title="Civilization VI",
    genre="Strategy",
    release_year=2016,
    rating=8.8
)

# Run the custom manager methods
action_games = VideoGame.objects.games_by_genre('Action')
recent_games = VideoGame.objects.recently_released_games(2019)
average_rating = VideoGame.objects.average_rating()
highest_rated = VideoGame.objects.highest_rated_game()
lowest_rated = VideoGame.objects.lowest_rated_game()

# Print the results
print("Action games:")
for game in action_games:
    print(f"- {game.title} ({game.genre}, {game.release_year}, Rating: {game.rating})")

print("\nRecently released games (2019+):")
for game in recent_games:
    print(f"- {game.title} ({game.release_year})")

print(f"\nAverage rating of all games: {average_rating}")

print(f"\nHighest rated game: {highest_rated.title} ({highest_rated.rating})")

print(f"Lowest rated game: {lowest_rated.title} ({lowest_rated.rating})")
