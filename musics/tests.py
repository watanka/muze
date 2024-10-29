from django.test import TestCase
from django.utils import timezone
from datetime import timedelta
from django.urls import reverse
from django.http import HttpResponse

from musics.models import Song
from django.contrib.auth import get_user_model
from unittest.mock import patch

User = get_user_model()


def create_song(title: str, album_cover: str, artist: str, genre: str, release_date: timezone):
    song = Song(title=title, artist=artist, genre=genre, release_date=release_date)
    if album_cover:
        song.album_cover = album_cover
    song.save()
    return song

def leave_comment(client, song, comment_text):
    post_comment = {
            'content': comment_text,
        }
    response = client.post(reverse('musics:comments', kwargs={'song_id': song.id}), 
                                    post_comment)

NOW = timezone.now().date()
YESTEREDAY = timezone.now().date() - timedelta(days = 1)
DAY_BEFORE_YESTERDAY = timezone.now().date() - timedelta(days = 2)


# Create your tests here.
class SongTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        
        # set up 3 songs by release date, num_likes, num_mention    

        num_mentions = [1, 3, 2] 
        num_likes = [1, 3, 2] 
        for i, release_date in enumerate([NOW, YESTEREDAY, DAY_BEFORE_YESTERDAY]):
            song = create_song(
                title=f'test_song_{i}',
                album_cover=f'album_cover_url_{i}.jpg',
                artist = f'test_artist_{i}',
                genre = 'pop',
                release_date = release_date
                )
            song.num_mention += num_mentions[i]
            song.num_likes += num_likes[i]
            song.save()

    def test_song_list_ordered_by_RELEASE_DATE(self):
        response = self.client.get(reverse('musics:index'), {'order': 'release_date'})
        self.assertEqual( response.context['song_list'][0].release_date, NOW)


    def test_song_list_ordered_by_NUM_MENTIONED(self):
        response = self.client.get(reverse('musics:index'), {'order': 'num_mentions'})
        
        # mention 수가 3개인 값이 가장 첫번째 배치
        self.assertEqual( response.context['song_list'][0].num_mention, 3)

    def test_song_list_ordered_by_NUM_LIKES(self):
        response = self.client.get(reverse('musics:index'), {'order': 'num_likes'})
        # mention 수가 3개인 값이 가장 첫번째 배치
        self.assertEqual( response.context['song_list'][0].num_likes, 3)

    def test_song_list_ordered_by_NUM_COMMENTS(self):
        self.client.login(username='testuser', password='testpassword')
        

        for num_comment in [1,100,2]:
            song = create_song(
                            title=f'test_song_with_comment_{num_comment}',
                            album_cover=f'album_cover_url.jpg',
                            artist = f'test_artist',
                            genre = 'pop',
                            release_date = timezone.now()
                            )
            for i in range(num_comment):
                leave_comment(self.client, song, f'TEST_COMMENT_{i}')
        
        response = self.client.get(reverse('musics:index'), {'order': 'num_comments'})
        self.assertEqual(response.context['song_list'][0].title, 
                         'test_song_with_comment_100')

    
    def test_no_comment(self):
        song = create_song(
                            title = "songtitle",
                            album_cover = "random_album_cover.png",
                            artist = "sample_artist",
                            genre = "POP",
                            release_date=timezone.now()
                            )
        response = self.client.get(reverse("musics:detail", args = (song.id,)))

        self.assertQuerySetEqual(response.context['comments'], [])

    @patch('musics.views.sp.search')
    def test_search_new_song(self, mock_search):
        data = {
            'category': 'track',
            'keyword': 'Test'
        }
        mock_search.return_value = {
            'tracks': {
                'items': [
                    {
                        'name': 'Test Track',
                        'popularity': 30,
                        'album': {
                            'name': 'Test Album',
                            'images': [{'url': 'http://example.com/image.jpg'}],
                            'release_date': '2023-01-01',
                        },
                        'artists': [{'name': 'Test Artist'}],
                        'external_urls': {'spotify': 'http://spotify.com/test'},
                    },
                ]
            }
        }
        response = self.client.post(reverse('musics:search'), data)

        self.assertEqual(response.status_code, 200)

        # 템플릿에 'musics/search_results.html'이 사용되었는지 확인합니다.
        self.assertTemplateUsed(response, 'musics/search_results.html')

        track_results = response.context['track_results']
        self.assertEqual(track_results[0]['title'], 'Test Track')

    '''
    새로운 노래를 요청하면, 검증과정을 거쳐 데이터베이스에 추가한다.
    검증과정: 이미 있는 노래인지 확인
    '''

    def test_request_new_song_fail_if_song_already_exists_in_db(self):
        '''
        새로운 노래 요청 시에, 이미 데이터베이스에 있는 곡이면 요청 실패 반환.
        '''
        data = {
            'track_name': 'Test Track',
            'album_cover': 'test_url',
            'artists': 'Test Artist',
            'release_date': '2024-10-21'
        }
        # 첫번째 요청 후 저장.
        self.client.post(reverse('musics:request_song'), data)
        # 똑같은 요청.
        response = self.client.post(reverse('musics:request_song'), data)
        
        self.assertIsInstance(response, HttpResponse)
        self.assertEqual(response.content.decode(), '곡이 이미 존재합니다.')
        