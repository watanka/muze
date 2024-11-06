
# Song title, 

class SearchAPIHandler:
    pass


class SpotifyAPIHandler(SearchAPIHandler):

    def __init__(self, api_client):
        self.api_client = api_client

    def search(self, query: str, category: str):
        
        # category는 title 또는 artist
        if category == 'title':
            category = 'track'
        
        api_result = self.api_client.search(q=f'{category}:{query}', type=category)
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
                "release_date": track['album']['release_date'],
                "image_url": track['album']['images'][0]['url']
            }
            artist_names = [artist['name'] for artist in track['artists']]
            spotify_url = track['external_urls']['spotify']
            result.append({
                'title': title,
                'track_popularity': track_popularity,
                'album': album_info,
                'artists': artist_names,
                'spotify_url': spotify_url
            })
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
                        'release_date':  album['release_date'],
                        'image_url': album['images'][0]['url']
                        }

            # 앨범의 트랙 가져오기
            tracks = self.api_client.album_tracks(album_id)
            for track in tracks['items']:
                track_title = track['name']
                track_id = track['id']
                track_popularity = self.api_client.track(track_id)['popularity']  # 각 트랙의 인기 점수 가져오기
                artist_names = ', '.join([artist['name'] for artist in track['artists']])
                spotify_url = track['external_urls']['spotify']
                all_tracks.append({
                    'title': track_title,
                    'track_popularity': track_popularity,
                    'album': album_info,
                    'artists': artist_names,
                    'spotify_url': spotify_url
                })
        return all_tracks