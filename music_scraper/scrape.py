import os, sys
import django
from django.core.exceptions import ObjectDoesNotExist
project_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if project_path not in sys.path:
    sys.path.append(project_path)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'music_dashboard.settings')
django.setup()
# Django 모델 임포트


import pandas as pd
from musics.models import Song
import spotipy
from datetime import datetime
from tqdm import tqdm
import time
from scrape import MusicCollector, persist

import base64

def encode_song_id(song_id):
    # song_id를 문자열로 변환하고 인코딩
    song_id_bytes = str(song_id).encode('utf-8')
    base64_bytes = base64.urlsafe_b64encode(song_id_bytes)
    return base64_bytes.decode('utf-8')  # Base64 문자열로 반환

def decode_song_id(encoded_song_id):
    # Base64 문자열을 디코드하여 원래의 song_id로 복원
    base64_bytes = encoded_song_id.encode('utf-8')
    song_id_bytes = base64.urlsafe_b64decode(base64_bytes)
    return int(song_id_bytes.decode('utf-8'))  # 정수로 변환하여 반환



class MusicCollector:

    def __init__(self, api_client):
        self.api_client = api_client

    def __call__(self, query, limit, time_sleep=1) -> pd.DataFrame:
        offset = 0
        track_results = []
        total_retrieved = 0
        while True:
            try:
                result = self.api_client.search(q=query, type='track', limit=limit, offset=offset)
                tracks = result['tracks']['items']
                if not tracks:
                    print('no more...')
                    break

                track_results.extend(tracks)
                total_retrieved += len(tracks)
                print(f'Retrieved {total_retrieved} tracks so far...')

                offset += limit
            except spotipy.exceptions.SpotifyException as e:
                print(f'Error occurred: {e}')
                break

        return track_results



def preprocess_data(tracks):
    artist_name_list=[]
    album_name_list = []
    track_name_list=[]
    track_popularity_list=[]
    track_image_url_list=[]
    release_dates_list = []
    track_id_list = []
    
    for track in tracks:  

        num_artists = len(track['artists'])
        artist_name = track['artists'][0]['name'] + f'외 {num_artists-1}명' if num_artists > 1 else  track['artists'][0]['name']
        track_name = track['name']

        # lookup unique_id는 {track_name}_{artist}로 설정한다.
        track_id_list.append(encode_song_id(track_name + '_' + artist_name))
        artist_name_list.append(track['artists'][0]['name'])
        album_name_list.append(track['album']['name'])
        track_name_list.append(track_name)
        track_popularity_list.append(track['popularity'])
        track_image_url_list.append(track['album']['images'][0]['url'])

        release_date = track['album']['release_date']
        if len(release_date.split('-')) == 1:
            release_date += '-01-01' # 무조건 1월 1일로 초기화
        release_dates_list.append(release_date) # 년도만 주어져있는 값들이 있음
        # print(track['name'])
        # print(f'Album: {track['album']['name']}\n{[artist['name'] for artist in track['artists']]}\ntrack_id:{track['id']}\ntrack_popularity: {track['popularity']}\nalbum_images:{track['album']['images'][0]['url']}\nRelease Date:{track['album']['release_date']}')
        # print('=========')

    track_df = pd.DataFrame({      
        'track_name' : track_name_list, 
        'track_id' : track_id_list, 
        'track_popularity' : track_popularity_list, 
        'artist_name' : artist_name_list, 
        'track_image_link': track_image_url_list,
        'release_date' : release_dates_list
        })
    return track_df


def persist(music_data):
    songs = []
    for _, row in music_data.iterrows():
        song = Song.objects.filter(title=row['track_name'], artist=row['artist_name']).first()
        if song is None:
            Song.objects.create(
                title = row['track_name'],
                artist = row['artist_name'],
                track_popularity = row['track_popularity'],
                album_cover = row['track_image_link'],
                release_date = datetime.strptime(row['release_date'], '%Y-%m-%d'), 
            )
            
        
    # Song.objects.bulk_create(songs)
