import http.client
import json
from urllib.parse import quote


from dataclasses import dataclass
from datetime import datetime
import abc

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
    @abc.abstractmethod
    def search(self, query: str):
        pass




class SpotifyAPIHandler(SearchAPIHandler):

    def __init__(self, api_client):
        self.api_client = api_client

    def __repr__(self):
        return 'Spotify API Handler'

    def search(self, query: str):
        
        # category는 title 또는 artist

        encoded_query = quote(query)
        api_result = self.api_client.search(q=f'track:{encoded_query}')
        print('api_result', api_result)
        # result 구조가 category에 따라 다름
        
        parsed_result = self.parse_track_result(api_result)
        
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
                    album_cover=album_info['image_url'],
                    api_name=self.__repr__()
                            )
                        )
        return result
    
        
    # def parse_artist_result(self, data):
        # 아티스트 검색
        if not data['artists']['items']:
            return []

        artist_id = data['artists']['items'][0]['id']
        print("Selected artist ID:", artist_id)  # 디버깅용


        # 아티스트의 앨범들 가져오기
        albums = self.api_client.artist_albums(artist_id, album_type='album')
        print("Albums:", albums)  # 디버깅용
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
            print("Tracks:", tracks)  # 디버깅용
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

    def search(self, query: str):
        encoded_query = quote(query)
        query = query.replace(' ', '-')
        try:
            self.conn.request("GET", f"/search?term={encoded_query}&offset=0&limit=5", headers=self.headers)
            response = self.conn.getresponse()
            api_result = json.loads(response.read().decode("utf-8"))
            return api_result
        finally:
            self.conn.close()
        

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
    
    # def parse_artist_result(self, data):
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
    
class YoutubeAPIHandler(SearchAPIHandler):
    def __init__(self):
        self.base_url = "www.googleapis.com"
        self.conn = http.client.HTTPSConnection(self.base_url)
        self.api_key = 'AIzaSyBNn4y2SlO9Blp3Lt_I5GLS1MPKJ-xtf5A'
        

    def __repr__(self):
        return 'Youtube API Handler'

    def search(self, query: str):
        encoded_query = quote(query)
        search_type = 'songs'
        # elif category == 'artists':
        #     search_type = 'artists'
        
        path = (f"/youtube/v3/search?"
               f"part=snippet"
               f"&q={encoded_query}"
               f"&type={search_type}"
               f"&maxResults=20"
               f"&key={self.api_key}")

        try:
            self.conn.request("GET", path)
            response = self.conn.getresponse()

            print("Response Headers:")
            for header, value in response.getheaders():
                print(f"{header}: {value}")
            api_result = json.loads(response.read().decode("utf-8"))
        finally:
            self.conn.close()

        self.parse_result(api_result)
        return api_result

    def parse_result(self, data):
        result = []
        if 'items' not in data:
            return result

        for item in data['items']:
            if item['id']['kind'] != 'youtube#video':
                continue
                
            snippet = item['snippet']
            video_id = item['id']['videoId']
            
            # 동영상 세부 정보 가져오기
            video_details = self.get_video_details(video_id)
            
            # 조회수를 가져오되, 없으면 0으로 설정
            try:
                view_count = int(video_details.get('statistics', {}).get('viewCount', 0))
            except (ValueError, TypeError):
                view_count = 0
            
            result.append(
                dict(
                    title=snippet.get('title', ''),
                    track_popularity=view_count,
                    album_name=snippet.get('channelTitle', ''),
                    release_date=snippet.get('publishedAt', '').split('T')[0],
                    artists=snippet.get('channelTitle', ''),
                    spotify_url=f"https://www.youtube.com/watch?v={video_id}",
                    album_cover=snippet.get('thumbnails', {}).get('high', {}).get('url', '')
                )
            )
        
        return result

    def get_video_details(self, video_id):
        path = (f"/youtube/v3/videos?"
               f"part=statistics"
               f"&id={video_id}"
               f"&key={self.api_key}")
        
        try:
            self.conn = http.client.HTTPSConnection(self.base_url)
            self.conn.request("GET", path)
            response = self.conn.getresponse()
            data = json.loads(response.read().decode("utf-8"))
            
            if 'items' in data and len(data['items']) > 0:
                return data['items'][0]
            return {}
        except Exception as e:
            print(f"Error getting video details: {e}")
            return {}
        finally:
            self.conn.close()

if __name__ == '__main__':
    import requests

    youtube_api_handler = YoutubeAPIHandler()
    # print(youtube_api_handler.search("power", 'title'))