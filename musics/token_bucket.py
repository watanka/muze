from .search_api_handler import SpotifyAPIHandler, ShazamAPIHandler, YoutubeAPIHandler
import time
import redis
from typing import Callable

class TokenBucket:
    def __init__(self, rate: int, capacity: int, api: Callable):
        self.rate = rate
        self.capacity = capacity
        self.tokens = capacity
        self.api = api
        self.last_filled = time.monotonic()
        self.redis_client = redis.Redis(
            host='localhost',  # Redis 서버 호스트
            port=6379,        # Redis 서버 포트
            db=0,            # 데이터베이스 번호
            decode_responses=True  # 문자열 응답 디코딩
        )

        # Redis에 초기 토큰 수와 마지막 채움 시간 설정
        api_name = self.api.__repr__()
        if not self.redis_client.exists(f"{api_name}_tokens"):
            self.redis_client.set(f"{api_name}_tokens", capacity)
            self.redis_client.set(f"{api_name}_last_filled", time.monotonic())


    def add_tokens(self):
        # Redis에서 현재 값들을 가져옴
        api_name = self.api.__repr__()
        current_tokens = float(self.redis_client.get(f"{api_name}_tokens"))
        last_filled = float(self.redis_client.get(f"{api_name}_last_filled"))
        
        now = time.monotonic()
        time_passed = now - last_filled
        tokens_to_add = time_passed * self.rate
        
        if tokens_to_add > 0:
            # 파이프라인을 사용하여 여러 작업을 원자적으로 실행
            pipe = self.redis_client.pipeline()
            new_tokens = min(self.capacity, current_tokens + tokens_to_add)
            pipe.set(f"{api_name}_tokens", new_tokens)
            pipe.set(f"{api_name}_last_filled", now)
            pipe.execute()


    def has_enough_tokens(self, tokens):
        api_name = self.api.__repr__()
        self.add_tokens()
        pipe = self.redis_client.pipeline()
        current_tokens = float(self.redis_client.get(f"{api_name}_tokens"))
        
        if current_tokens >= tokens:
            pipe.set(f"{api_name}_tokens", current_tokens - tokens)
            pipe.execute()
            return True
        return False


class ApiManager:
    def __init__(self, apis):
        self.api_buckets = {api.__repr__(): TokenBucket(rate, capacity, api) for api, rate, capacity in apis}

    def call_api(self, api_name):
        bucket = self.api_buckets.get(api_name)
        if bucket and bucket.has_enough_tokens(1):
            print(f'API {api_name} called successfully')
        else:
            print(f'API {api_name} rate limit exceeded')

    def get_most_available_api(self):
        # 각 API의 남은 토큰 수를 기준으로 내림차순 정렬하여 가장 많이 남은 API 선택
        sorted_apis = sorted(
            self.api_buckets.items(),
            key=lambda item: item[1].tokens,
            reverse=True
        )
        
        
        for api_name, bucket in sorted_apis:
            if bucket.has_enough_tokens(1):
                return api_name
        return None  

    def distribute_requests(self, query, category):
        while True:
            # 남은 토큰이 가장 많은 API를 선택하여 호출
            api_name = self.get_most_available_api()
            if api_name:

                print(f"API '{api_name}' 호출 성공")
                return self.api_buckets[api_name].api.search(query, category)
            else:
                print("모든 API가 rate limit에 도달했습니다. 대기 중...")
                
            time.sleep(0.1)  # 호출 간격 (테스트용)

import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials


client_id = os.getenv('SPOTIFY_CLIENT_ID', '5739434950d9404a8d332c07d98d1914')
client_secret = os.getenv('SPOTIFY_CLIENT_SECRET', '0a0d268d4c2d4f5983dd583c47cdaecd')


client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)


spotify_api_handler =  SpotifyAPIHandler(sp)
shazam_api_handler = ShazamAPIHandler()
youtube_api_handler = YoutubeAPIHandler()


apis = [
    (spotify_api_handler, 3, 10),
    (shazam_api_handler, 2, 10),
    (youtube_api_handler, 1, 10)
]

api_manager = ApiManager(apis)
