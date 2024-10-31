# import time
# import spotipy
# from spotipy.oauth2 import SpotifyClientCredentials
# from scrape import MusicCollector
# import pandas as pd
# import os


# if __name__ == '__main__':
#     client_id = os.getenv('SPOTIFY_CLIENT_ID')
#     client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')

#     client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
#     sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)


#     collector = MusicCollector(api_client = sp)

#     ####################################
#     # Spotify API 사용하여 음악정보 수집 #
#     ####################################

#     tracks = collector(query="year:1950-1951", limit = 50)
#     print(f"Total tracks retrieved: {len(tracks)}")
