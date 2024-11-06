from celery import shared_task
from musics.models import Song

@shared_task
def persist(title, track_popularity, artists, album, release_date, album_cover):
    Song.objects.create(
        title = title,
        track_popularity = track_popularity,
        artist = artists,
        album = album,
        album_cover = album_cover,
        release_date = release_date
    )
    print('곡 저장 완료')

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