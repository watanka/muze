import http.client
import json
from urllib.parse import quote


from dataclasses import dataclass
from datetime import datetime


@dataclass
class SearchResult:
    title: str
    track_popularity: int
    album_name: str
    release_date: datetime
    artists: str
    spotify_url: str
    album_cover: str


# Song title, 

class SearchAPIHandler:
    pass


class SpotifyAPIHandler(SearchAPIHandler):

    def __init__(self, api_client):
        self.api_client = api_client

    def __repr__(self):
        return 'Spotify API Handler'

    def search(self, query: str, category: str):
        
        # category는 title 또는 artist
        if category == 'title':
            category = 'track'
        if category == 'artists':
            category = 'artist'

        encoded_query = quote(query)
        api_result = self.api_client.search(q=f'{category}:{encoded_query}', type=category)
        # result 구조가 category에 따라 다름
        
        if category == 'track':
            parsed_result = self.parse_track_result(api_result)
        elif category == 'artist':
            parsed_result = self.parse_artist_result(api_result)

        '''
          parsed_result 구조는
          title
          track_popularity
          album
          artists
          spotify_url
        '''
        return parsed_result


        
    def parse_track_result(self, data):
        result = []
        ## 3개만
        for track in data['tracks']['items'][:3]:
            title = track['name']
            track_popularity = track['popularity']
            album_info = {
                "name": track['album']['name'],
                "release_date": str(track['album']['release_date']),
                "image_url": track['album']['images'][0]['url']
            }
            artist_names = ', '.join([artist['name'] for artist in track['artists']])
            spotify_url = track['external_urls']['spotify']
            result.append(
                dict(
                    title=title, 
                    track_popularity=track_popularity,
                    album_name=album_info['name'],
                    release_date=album_info['release_date'],
                    artists=artist_names,
                    spotify_url=spotify_url,
                    album_cover=album_info['image_url']
                            )
                        )
        return result
    
        
    def parse_artist_result(self, data):
        # 아티스트 검색
        if not data['artists']['items']:
            return []

        artist_id = data['artists']['items'][0]['id']
        

        # 아티스트의 앨범들 가져오기
        albums = self.api_client.artist_albums(artist_id, album_type='album')
        all_tracks = []

        for album in albums['items']:
            album_id = album['id']
            album_name = album['name']
            album_info = {'name': album_name,
                        'release_date':  str(album['release_date']),
                        'image_url': album['images'][0]['url']
                        }

            # 앨범의 트랙 가져오기
            tracks = self.api_client.album_tracks(album_id)
            for track in tracks['items']:
                title = track['name']
                track_id = track['id']
                track_popularity = self.api_client.track(track_id)['popularity']  # 각 트랙의 인기 점수 가져오기
                artist_names = ', '.join([artist['name'] for artist in track['artists']])
                spotify_url = track['external_urls']['spotify']
                all_tracks.append(
                        dict(title=title, 
                        track_popularity=track_popularity,
                        album_name=album_info['name'],
                        release_date=album_info['release_date'],
                        artists=artist_names,
                        spotify_url=spotify_url,
                        album_cover=album_info['image_url']
                            ))
        return all_tracks


class ShazamAPIHandler(SearchAPIHandler):
    def __init__(self):
        self.conn = http.client.HTTPSConnection("shazam.p.rapidapi.com")
        self.headers = {
            'x-rapidapi-key': 'f07ef3a8eemshe16a5da51692d69p1965b1jsn532a39fb855c',
            'x-rapidapi-host': "shazam.p.rapidapi.com"
        }

    def __repr__(self):
        return 'Shazam API Handler'

    def search(self, query: str, category: str):
        encoded_query = quote(query)
        query = query.replace(' ', '-')
        try:
            self.conn.request("GET", f"/search?term={encoded_query}&offset=0&limit=5", headers=self.headers)
            response = self.conn.getresponse()
            api_result = json.loads(response.read().decode("utf-8"))
        finally:
            self.conn.close()
        if category == 'title':
            return self.parse_track_result(api_result)
        elif category == 'artists':
            return self.parse_artist_result(api_result)

        

    def parse_track_result(self, data):
        result = []
        # Shazam API 응답에서 tracks 부분 파싱
        tracks = data.get('tracks', {}).get('hits', [])[:3]  # 상위 3개만
        
        for track_hit in tracks:
            track = track_hit.get('track', {})
            
            # 앨범 이미지 URL 가져오기
            images = track.get('images', {})
            album_cover = images.get('coverarthq', '')
            
            
            result.append(
                dict(
                    title=track.get('title', ''),
                    track_popularity=50,  # Shazam은 인기도를 제공하지 않아 기본값 설정
                    album_name=track.get('subtitle', ''),  # 또는 앨범 정보가 있다면 그것을 사용
                    release_date=track.get('releasedate', datetime.now().strftime('%Y-%m-%d')),
                    artists=track.get('subtitle', ''),  # artist 정보
                    spotify_url=track.get('url', ''),  # Shazam URL
                    album_cover=album_cover
                )
            )
        return result
    
    def parse_artist_result(self, data):
        result = []
        # Shazam API 응답에서 tracks 부분 파싱
        tracks = data.get('tracks', {}).get('hits', [])[:3]  # 상위 3개만
        
        for track_hit in tracks:
            track = track_hit.get('track', {})
            
            release_date = track.get('releasedate', datetime.now().strftime('%Y-%m-%d'))
            # 필요한 정보만 추출
            result.append(
                dict(
                    title=track.get('title', ''),
                    track_popularity=50,  # Shazam은 인기도를 제공하지 않아 기본값 설정
                    album_name=track.get('subtitle', ''),  # artist 정보가 subtitle에 있음
                    release_date=track.get('releasedate', datetime.now().strftime('%Y-%m-%d')),  # Shazam API는 발매일 정보 제공하지 않음
                    artists=track.get('subtitle', ''),  # artist 정보
                    spotify_url=track.get('url', ''),  # Shazam URL
                    album_cover=track.get('images', {}).get('coverarthq', '')
                )
            )
        
        return result