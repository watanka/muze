from django.http import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404
from .models import Song

def index(request):
    latest_song_list = Song.objects.order_by("-release_date")[:5]
    return render(request, 'musics/index.html', {'latest_song_list': latest_song_list})


def detail(request, song_id):
    song = get_object_or_404(Song, id = song_id)
    comments = song.comments.all()
    context = {
        'song': song,
        'comments': comments
    }
    return render(request, 'musics/detail.html', context)

def comments(request, song_id):
    pass
def likes(request, song_id):
    pass