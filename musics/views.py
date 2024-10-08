from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader
from .models import Song

def index(request):
    latest_song_list = Song.objects.order_by("-release_date")[:5]
    template = loader.get_template('musics/index.html')
    
    context = {'latest_song_list': latest_song_list}
    return HttpResponse(template.render(context, request))


def detail(request, song_id):
    pass
def comments(request, song_id):
    pass

def likes(request, song_id):
    pass