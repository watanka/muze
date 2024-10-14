import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd

import os
import django
# Django settings 모듈 설정
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'music_dashboard.settings')

# Django 초기화
django.setup()

# Django 모델 임포트
from musics.models import Song
from tqdm import tqdm

client_id = '5739434950d9404a8d332c07d98d1914'
client_secret = '0a0d268d4c2d4f5983dd583c47cdaecd'


client_credentials_manager = SpotifyClientCredentials(client_id= client_id, client_secret= client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

artist_name=[]
artist_id=[]
track_name=[]
track_id=[]
track_popularity=[]
track_images=[]
release_dates = []

for i in tqdm(range(0, 1000, 50)):
    track_results = sp.search(q=f"year:2020-2024", market='KR', type="track", limit=50, offset=i)
    for _, t in enumerate(track_results['tracks']['items']):
        artist_name.append(t['artists'][0]['name'])
        artist_id.append(t['artists'][0]['id'])
        track_name.append(t['name'])
        track_id.append(t['id'])
        track_popularity.append(t['popularity'])
        track_images.append(t['album']['images'][0]['url'])
        release_dates.append(t['album']['release_date'])
    

track_df = pd.DataFrame({'track_name' : track_name, 
                         'track_id' : track_id, 
                         'track_popularity' : track_popularity, 
                         'artist_name' : artist_name, 
                         'artist_id' : artist_id, 
                         'track_image_link': track_images,
                         'release_date' : release_dates
                         })
track_df.to_csv('sample.csv')

def persist(music_data):
    songs = []
    for _, row in music_data.iterrows():
        
        songs.append(
            Song(
                title = row['track_name'],
                artist = row['artist_name'],
                album_cover = row['track_image_link'],
                release_date = row['release_date']
                )
            )
        
        
        
    Song.objects.bulk_create(songs)

persist(track_df)