## 음악 취향을 공유하는 음악추천 서비스

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
- saved
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