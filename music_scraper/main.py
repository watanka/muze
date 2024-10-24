import time
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from scrape import MusicCollector
import pandas as pd


if __name__ == '__main__':
    client_id = '5739434950d9404a8d332c07d98d1914'
    client_secret = '0a0d268d4c2d4f5983dd583c47cdaecd'

    client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)


    collector = MusicCollector(api_client = sp)

    ####################################
    # Spotify API 사용하여 음악정보 수집 #
    ####################################

    tracks = collector(query="year:1950-1951", limit = 50)
    print(f"Total tracks retrieved: {len(tracks)}")
