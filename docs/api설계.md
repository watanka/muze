### 스토리보드를 기반으로 필요한 API를 정의한다.

#### 유저
- `users/{user_id}/profile`, `GET`, 유저 프로필 조회
- `users/{receiver_id}/add_friend` body={sender_id}, `POST`, 유저 친구 추가
- `users/{receiver_id}/friend_request`, `GET`, 친구 요청 조회
- `users/{receiver_id}/friend_request/{sender_id}`, `GET`, 친구 요청 디테일 조회
- `users/{user_id}/feed`, `GET`, 유저 피드 조회
- `users/{user_id}/inbox`, `GET`, 메세지 조회
- `users/{user_id}/set-todays-song/`, `POST`, body={'song_id'}, '오늘의 노래' 지정
- `users/{user_id}/liked_songs`, `GET`, like한 노래 조회
- `users/{user_id}/saved_songs`, `GET`, 저장한 노래 조회

#### 노래
- `songs/{song_id}/like`, `POST`, 노래 like
- `songs/{song_id}/share`, body = {'user_id', 'friend_id', 'message'}, `POST`, 노래 친구에게 공유
- `songs/{song_id}/comments/`, body = {'user_id', 'contents'}, `POST`, 댓글 달기
- `songs/{song_id}/save`, body = {'user_id'}, 노래 저장

#### 검색
`/search/songs` param = {'q', 'artist'}, `GET`, 노래 검색
`/search/users` param = {'q' }, `GET`, 유저 검색