## User(유저)
- id: 유저 고유 ID (Primary Key)
- nickname: 사용자 닉네임
- profile_picture_url: 프로필 사진 URL
- today_song_id: 오늘의 노래 ID (Foreign Key, 노래 테이블 참조)
- liked_songs: 좋아한 노래 목록 (ManyToManyField 또는 별도의 테이블)
- saved_songs: 저장한 노래 목록 (ManyToManyField 또는 별도의 테이블)
- shared_songs: 공유한 노래 목록 (ManyToManyField 또는 별도의 테이블)
- friends: 친구 목록 (ManyToManyField, 같은 User 모델 참조)

## Song
- id: 노래 고유 ID (Primary Key)
- title: 노래 제목
- artist: 아티스트 이름
- genre: 장르
- album: 앨범
- num_mentions: 노래 언급 횟수 (사용자에 의해 공유된 횟수)
- num_likes: 좋아요 수 (좋아요를 받은 횟수)
- release_date: 노래 등록 날짜 (추가 필드, 선택적)
- updated_at: 노래 정보 업데이트 날짜 (추가 필드, 선택적)

## Comment
- id: 댓글 고유 ID (Primary Key, 추가)
- song_id: 노래 ID (Foreign Key, Song 모델 참조)
- user_id: 유저 ID (Foreign Key, User 모델 참조)
- content: 댓글 내용
- created_at: 댓글 작성 날짜
- updated_at: 댓글 수정 날짜 (추가 필드, 선택적)

## UserActivity
- id: 고유 ID (Primary Key)
- user_id: 유저 ID (Foreign Key, User 모델 참조)
- activity_type: 활동 유형 (ENUM: 'like', 'save', 'share', 'set_today_song')
- song_id: 노래 ID (Foreign Key, Song 모델 참조, NULL 가능)
- friend_user_id: 친구 유저 ID (Foreign Key, User 모델 참조, NULL 가능)
- created_at: 활동 발생 날짜