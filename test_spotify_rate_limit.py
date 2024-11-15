import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import requests



client_id = os.getenv('SPOTIFY_CLIENT_ID', '5739434950d9404a8d332c07d98d1914')
client_secret = os.getenv('SPOTIFY_CLIENT_SECRET', '0a0d268d4c2d4f5983dd583c47cdaecd')

# client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
# sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
def search_with_requests():
    # 인증 설정
    client_credentials_manager = SpotifyClientCredentials(
        client_id=client_id,
        client_secret=client_secret
    )
    
    # 액세스 토큰 얻기
    token = client_credentials_manager.get_access_token()
    
    # API 요청
    headers = {
        'Authorization': f'Bearer {token["access_token"]}'
    }
    
    response = requests.get(
        'https://api.spotify.com/v1/search',
        params={
            'q': 'artist:IU',
            'type': 'artist'
        },
        headers=headers
    )
    
    return {
        'status_code': response.status_code,
        'response': response.json()
    }


# result = search_with_requests()
# print(f"Status Code: {result['status_code']}")


# for i in range(10000):
#     print(f'{i}번째 요청 결과: ', search_with_requests()['status_code'])
        

from concurrent.futures import ThreadPoolExecutor, as_completed
import time
import sys

def print_progress(completed, total, elapsed_time):
    """진행 상황을 같은 줄에 업데이트하여 출력"""
    sys.stdout.write('\r')  # 커서를 줄 시작으로 이동
    sys.stdout.write(f"Progress: {completed}/{total} | Time: {elapsed_time:.2f}s")
    sys.stdout.flush()  # 버퍼 즉시 출력

def test_rate_limit(total_requests, duration=5, max_workers=5):
    """
    지정된 시간 동안 정해진 수의 요청을 보내는 테스트 함수
    
    Args:
        total_requests (int): 보낼 총 요청 수
        duration (int): 테스트 진행 시간 (초)
        max_workers (int): 동시에 실행할 최대 쓰레드 수
    """
    results = []
    start_time = time.time()
    
    # 테스트용 쿼리 생성
    queries = [f"artist:IU" for _ in range(total_requests)]
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # 모든 쿼리에 대한 future 생성
        future_to_query = {
            executor.submit(search_with_requests): query 
            for query in queries
        }
        
        # future가 완료될 때마다 결과 처리
        for future in as_completed(future_to_query):
            query = future_to_query[future]
            try:
                result = future.result()
                results.append(result)
                
                # 현재 진행 상황 출력
                elapsed_time = time.time() - start_time
                print_progress(len(results), total_requests, elapsed_time)
                
                
                # 지정된 시간이 지나면 중단
                if elapsed_time >= duration:
                    for f in future_to_query:
                            if not f.done():
                                f.cancel()
                    break
                
            except Exception as e:
                print(f"Search failed for {query}: {str(e)}")

    return results

def trial(max_requests, duration, max_workers):
    print(f'trial: {max_workers} workers, duration: {duration} seconds, max_requests: {max_requests}')
    results = test_rate_limit(
                total_requests=max_requests,  
                duration=duration,         
                max_workers=max_workers 
            )

    successes = sum(1 for r in results if r['status_code'] == 200)
    failures = sum(1 for r in results if r['status_code'] != 200)

    print(f"\n총 검색: {len(results)}")
    print(f"성공: {successes}")
    print(f"실패: {failures}")

    return {
        'num_requests': len(results),
        'num_success': successes,
        'num_failures': failures
    }


def experiment(max_workers_list, request_duration, interval_btw_experiment):
    experiment_results = []
    for max_workers in max_workers_list:
        experiment_results.append(trial(max_requests=10000, duration=request_duration, max_workers=max_workers))
        print(f'break for {interval_btw_experiment} seconds...')
        time.sleep(interval_btw_experiment)
    
    return experiment_results

# 사용 예시
if __name__ == "__main__":
    # 30초 동안 100개의 요청을 5개의 쓰레드로 실행

    max_workers_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    interval_btw_experiment = 50
    request_duration = 30 # spotify api rate limiting rolling window size

    
    experiment_results = experiment(max_workers_list, request_duration, interval_btw_experiment)
    print(experiment_results)
        