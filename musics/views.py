from typing import Any
from django.http import HttpResponse, Http404, JsonResponse
from django.urls import reverse
from django.db.models import Count
from django.views.generic import ListView, DetailView, View
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .models import Song, TodaySong, Comment
from .form import CommentForm, SearchForm
from music_dashboard.tasks import celery_save_db

from dataclasses import asdict

import logging

logger = logging.getLogger('django')

class SongListView(ListView):
    model = Song
    template_name = "musics/index.html"
    context_object_name = "song_list"
    paginate_by=20

    def get_queryset(self):
        queryset = Song.objects.all()  # 기본 쿼리셋

        order_by = self.request.GET.get('order', 'popularity')  # 정렬 기준, 기본은 popularity
        if order_by == 'release_date':
            logger.info("Song 전체 목록 최신순")
            queryset = queryset.order_by('-release_date')  # 최신순
        elif order_by == 'num_likes':
            logger.info("Song 전체 목록 like순")
            queryset = queryset.order_by('-num_likes')  # 인기순
        elif order_by == 'num_mentions':
            logger.info("Song 전체 목록 mention순")
            queryset = queryset.order_by('-num_mention')
        # 다른 정렬 조건도 추가 가능
        elif order_by == 'num_comments':
            logger.info("Song 전체 목록 comment순")
            queryset = queryset.annotate(num_comments=Count('comments')).order_by('-num_comments')
        return queryset
    
    def render_to_response(self, context: dict[str, Any], **response_kwargs: Any) -> HttpResponse:
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            songs_html = self.render_to_string('musics/_song_list.html', {'song_list': context['song_list']})
            return JsonResponse({'html': songs_html})
        
        return super().render_to_response(context, **response_kwargs)

class SongDetailView(DetailView):
    model = Song
    template_name = "musics/detail.html"
    context_object_name = "song"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        logger.info(f'User: {self.request.user} Song {self.object.title} detail 조회')
        context['comments'] = self.object.comments.all()
        return context

@method_decorator(login_required, name='dispatch')  # 모든 메서드에 대해 로그인 요구
class CommentView(View):
    def get(self, request, song_id):
        song = get_object_or_404(Song, id=song_id)
        comments = song.comments.all()  # song에 연결된 댓글 가져오기
        return render(request, "musics/comments.html", 
                      {'song': song, 'comments': comments})

    def post(self, request, song_id):
        user = request.user
        song = get_object_or_404(Song, id=song_id)
        form = CommentForm(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.song = song
            new_comment.user = user
            new_comment.save()
            return redirect(reverse('musics:detail', args=(song_id,)))
        # 유효하지 않은 폼일 경우 댓글 목록과 함께 다시 렌더링
        comments = song.comments.all()
        return redirect(reverse('musics:detail', args=(song.id,)))
    
    # render(request, "musics/comments.html", {'song': song, 'comments': comments, 'form': form})
    
    def get_queryset(self):
        song_id = self.kwargs['song_id']
        return Comment.objects.filter(song__id=song_id).order_by('-created_at')  # 특정 Song에 연결된 댓글만 가져옴

@login_required
def likes(request, song_id):
    song = get_object_or_404(Song, id=song_id)
    
    user_profile = request.user
    if song in user_profile.liked_songs.all():
        # 유저가 이미 이 곡을 좋아요 했을 경우
        return redirect(reverse('musics:detail', args=[song_id]))

    song.num_likes += 1
    song.save(update_fields=['num_likes'])
    user_profile.liked_songs.add(song)

    return redirect(reverse('musics:detail', args=(song_id,)))

import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

client_id = os.getenv('SPOTIFY_CLIENT_ID')
client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')

client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

from .search_api_handler import SpotifyAPIHandler,ShazamAPIHandler

api_handler = ShazamAPIHandler()


def search_view(request):
    # 검색한 카테고리의 쿼리가 DB에 없는지 확인
    # 없을 경우 API 호출
    if request.method == 'GET':
        form = SearchForm(request.GET)
        if form.is_valid():
            category = form.cleaned_data['category']
            keyword = form.cleaned_data['keyword']

            db_result = Song.objects.filter(**{f'{category}__icontains': keyword})
            # DB 결과에 있을 경우; DB 결과는 리턴되도 원하는 결과가 아닐 수 있음. 예) 같은 제목 다른 아티스트
            if db_result.exists():
                return render(request, 'musics/search_results.html', {'track_results': db_result})
            print('search 진행 from view')
            search_result = api_handler.search(keyword, category)
            
            print('search_result', search_result)
            for res in search_result:
                celery_save_db.delay(res)
            
            return render(request, 'musics/search_results.html', {'track_results': search_result})
    else:
        form = SearchForm()
    return render(request, 'musics/search.html', {'form': form})

@login_required
def add_today_song(request):
    song_id = request.POST.get('song_id')
    song = get_object_or_404(Song, pk=song_id)
    today_song = TodaySong.objects.create(
        song = song,
        user = request.user
    )
    today_song.save()

    song.num_mention += 1
    song.save()
    return JsonResponse({'success': True})