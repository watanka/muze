from django.test import TestCase
from django.utils import timezone
from django.urls import reverse
from musics.models import Song, Comment


def create_song(title: str, album_cover: str, artist: str, genre: str, release_date: timezone):
    song = Song(title=title, artist=artist, genre=genre, release_date=release_date)
    if album_cover:
        song.album_cover = album_cover
    song.save()
    return song

# Create your tests here.
class SongTests(TestCase):
    def test_no_song_is_displayed(self):
        response = self.client.get(reverse("musics:index"))
        self.assertQuerySetEqual(response.context["latest_song_list"], [])

    def test_default_album_cover_is_used_when_not_given(self):
        song = create_song(
                                title = "songtitle",
                                album_cover = None,
                                artist = "sample_artist",
                                genre = "POP",
                                release_date=timezone.now()
                            )
        response = self.client.get(reverse("musics:detail", args = (song.id,)))
        self.assertEqual(response.context['song'].album_cover, 'default_albumcover.png')

    def test_no_comment(self):
        song = create_song(
                                title = "songtitle",
                                album_cover = "random_album_cover.png",
                                artist = "sample_artist",
                                genre = "POP",
                                release_date=timezone.now()
                            )
        response = self.client.get(reverse("musics:detail", args = (song.id,)))

    def test_comment_on_a_question(self):
        song = create_song(
                                title = "songtitle",
                                album_cover = "random_album_cover.png",
                                artist = "sample_artist",
                                genre = "POP",
                                release_date=timezone.now()
                            )
        
        