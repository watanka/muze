from celery import shared_task

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from datetime import datetime

from ..music_scraper.scrape import MusicCollector, preprocess_data, persist

client_id = '5739434950d9404a8d332c07d98d1914'
client_secret = '0a0d268d4c2d4f5983dd583c47cdaecd'

client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)


collector = MusicCollector(api_client = sp)

@shared_task
def collect():
    print('collecting music begin!')
    tracks = collector(query=f'year:{datetime.now().year}')
    track_df = preprocess_data(tracks)
    persist(track_df)