## 음악 취향을 공유하는 음악추천 서비스

### TODO
- [ ] scheduling job - 음악 크롤링
- [ ] error handling
- [ ] logging
- [ ] monitoring
- [ ] microservice
- [ ] User와 UserProfile이 분리되어있기 때문에, 둘 중 하나 생성시 같이 생성될 수 있도록 설정해야함.
- [ ] Song에다가 message 기능 추가하기




### 요구사항 정의
- [ ] 음악은 유저가 직접 업로드하거나 삭제할 수 없다.


#### schema
Song
- genre
- artist
- album
- cover(img)
- lyrics
- release date
- rate

User
- saved_song
- comments
- mates


#### api endpoint
`/musics`
- `GET`, / , ?sort={genre, rate, new-released}, 음악 나열
- `POST`, / , Song, 새로운 음악 추가(관리자만 사용가능)
- `GET`, <int:song_id>/comments, 해당 음악의 댓글 확인
- `POST`, <int:song_id>/comments, 해당 음악의 댓글 추가
- `GET`, <int:song_id>/likes, 해당 음악의 라이크 수 조회
- `POST`, <int:song_id>/likes, 해당 음악의 라이크 추가(한 번더 누를 경우 취소)

`/users`
- send song to another user
- `GET`, view mates
- `GET`, 다른 유저들과의 compatibility 확인


#### 음악 정보 수집
음악 정보 수집 API -> Django DB 저장 -> scheduling 반복

#### OAuth

client - web server  
web server -> form to access auth server -> client   
client -> auth server  
auth server -> give token to client  


#### 음악 정보 Display 기준
- 장르별
- 최신별
- 인기별
- liked_song, mentioned_song, save_song 기준 추천별



오늘의 노래는 24시간 유지된다. 24시간 후에는 삭제.
이 삭제 시점을 어떻게 가져가야할지? 조회 시?


[API 다중화](docs/데이터수집.md)  


데이터베이스 최적화  

부하 테스트