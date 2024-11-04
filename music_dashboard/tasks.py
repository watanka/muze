from celery import shared_task
from musics.models import Song

@shared_task
def persist(title, track_popularity, artists):
    Song.objects.create(
        title = title,
        track_popularity = track_popularity,
        artist = artists,

    )

@shared_task
def celery_plus(num1, num2):
    return num1 + num2

# from ..music_scraper.scrape import MusicCollector, preprocess_data, persist


# client_id = os.getenv('SPOTIFY_CLIENT_ID')
# client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')

# client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
# sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)


# collector = MusicCollector(api_client = sp)

# @shared_task
# def collect():
#     print('collecting music begin!')
#     tracks = collector(query=f'year:{datetime.now().year}')
#     track_df = preprocess_data(tracks)
#     persist(track_df)