from celery import shared_task
from musics.search_api_handler import SearchResult
from musics.models import Song
from users.models import UserActivity
from dataclasses import asdict

@shared_task
def celery_save_song(data: SearchResult):
    Song.objects.create(**data)


@shared_task
def celery_save_user_activity(*data):
    UserActivity.objects.create(*data)

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