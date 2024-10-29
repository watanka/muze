Spotify API를 사용해서 '노래' 정보들을 읽어온다.  
'노래'에 들어가는 정보는 다음과 같다.  
- artist_name
- track_name
- track_popularity
- track_images
- release_date

'노래'는 매일 업데이트된다.  
업데이트를 주기적으로 반영하기 위해 작성한 `scrape.py` 코드를 스케쥴러로 돌린다.


#### 노래 정보 처음부터 끝까지 다 읽는 방법
1. track_id의 순서를 찾아서 처음부터 끝까지 다 읽는다. -> 트랙 ID 패턴을 찾아야함 -> ID 패턴 찾기 쉽지 않음 X
2. genre별로 모든 곡을 찾는다. 모든 곡을 어떻게 찾음? 각 장르마다 몇 개씩있는지 알아야되나? 여러 장르에 속한 노래들도 있을텐데 X
3. 기간별로 찾을 수 있는 노래들을 전부 다 찾는다. -> 최대한 숫자를 크게 해서. 1000만 곡 이런식으로? -> 새로운 곡 읽어올 때, 최신년도 기준으로 읽어오면됨.

#### 주의사항
- 긁어올때, 주의사항 일정 속도 이상으로 긁을경우 rate_limit에 걸릴 수 있음.
- offset=50일 때, 항상 100번째 때 error 발생
```
  File "/root/.cache/pypoetry/virtualenvs/music-dashboard-_wBOlSh5-py3.12/lib/python3.12/site-packages/spotipy/client.py", line 297, in _internal_call   
    raise SpotifyException(
spotipy.exceptions.SpotifyException: http status: 400, code:-1 - https://api.spotify.com/v1/search?q=year%3A2022-2024&limit=10&offset=1000&type=track:   
 Bad request., reason: None
 ```

최신정보를 불러오는 방법
- 기존 정보 확인
- 변경 사항 확인
- 변경사항만 업데이트


1. 데이터베이스 연결확인
2. 스케쥴링화
3. celery로 분산 처리
4. scheduling -> message broker -> consumer(celery) 


메세지큐에 등록하여, 노래를 찾을 수 있도록 구성.

