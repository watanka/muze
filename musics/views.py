from django.http import HttpResponse, Http404, JsonResponse
from django.urls import reverse
from django.db.models import Count
from django.core.exceptions import ValidationError
from django.views.generic import ListView, DetailView, View
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .models import Song, TodaySong, Comment
from .token_bucket import api_manager
from .form import CommentForm, SearchForm
from music_dashboard.tasks import celery_save_song, celery_save_user_activity

from typing import Any
from datetime import timedelta
from dataclasses import asdict
import logging

logger = logging.getLogger('django')

class SongListView(ListView):
    model = Song
    template_name = "musics/index.html"
    context_object_name = "song_list"
    paginate_by=20

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = SearchForm(self.request.GET or None)
        return context

    def get_queryset(self):
        order_by = self.request.GET.get('order', 'release_date')  # 정렬 기준, 기본은 최신순
        return Song.objects.list_by(order_by)

    
    def render_to_response(self, context: dict[str, Any], **response_kwargs: Any) -> HttpResponse:
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            songs_html = self.render_to_string('musics/song_list.html', {'song_list': context['song_list']})
            return JsonResponse({'html': songs_html})
        
        return super().render_to_response(context, **response_kwargs)

class SongDetailView(DetailView):
    template_name = "musics/detail.html"
    context_object_name = "song"

    def get_queryset(self):
        return Song.objects.prefetch_related('comments')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        logger.info(f'User: {self.request.user} Song {self.object.title} detail 조회')
        context['comments'] = self.object.comments.all()
        context['is_today_song'] = False

        if self.request.user.is_authenticated:
            latest_today_song = TodaySong.objects.filter(
                user=self.request.user,
                song=self.object
                ).order_by('-created_at').first()
            if latest_today_song:
                context['is_today_song'] = latest_today_song.is_active()

        return context

 
class CommentView(View):
    def get(self, request, song_id):
        song = get_object_or_404(Song, id=song_id)
        comments = song.comments.all()  # song에 연결된 댓글 가져오기
        return render(request, "musics/comments.html", 
                      {'song': song, 'comments': comments})
    
    @method_decorator(login_required)
    def post(self, request, song_id):
        user = request.user
        song = get_object_or_404(Song, id=song_id)
        form = CommentForm(request.POST)
        if form.is_valid():
            Comment.objects.save_comment(song, user, form.cleaned_data['content'])
            celery_save_user_activity.delay(user.id, 'comment', song.id)

            return redirect(reverse('musics:detail', args=(song_id,)))
        return redirect(reverse('musics:detail', args=(song.id,)))

    def get_queryset(self):
        song_id = self.kwargs['song_id']
        return Comment.objects.filter(song__id=song_id).order_by('-created_at')  # 특정 Song에 연결된 댓글만 가져옴

@login_required
def likes(request, song_id):
    song = get_object_or_404(Song, id=song_id)
    user_profile = request.user
    try:
        user_profile.like_song(song)
        song.add_num_likes()
    except ValidationError as e:
        return redirect(reverse('musics:detail', args=[song_id]), {'error': str(e)})

    celery_save_user_activity.delay(user_profile.id, 'like', song.id)

    return redirect(reverse('musics:detail', args=(song_id,)))


def search_view(request):
    # 검색한 카테고리의 쿼리가 DB에 없는지 확인
    # 없을 경우 API 호출
    if request.method == 'GET':
        form = SearchForm(request.GET)
        if form.is_valid():
            category = form.cleaned_data['category']
            keyword = form.cleaned_data['keyword']

            db_result = Song.objects.search(keyword, category)
            # DB 결과에 있을 경우; DB 결과는 리턴되도 원하는 결과가 아닐 수 있음. 예) 같은 제목 다른 아티스트
            if db_result.exists():
                return render(request, 'musics/search_results.html', {'track_results': db_result})
            
            search_result = api_manager.distribute_requests(keyword, category)
            
            
            for res in search_result:
                celery_save_song.delay(res)
            
            return render(request, 'musics/search_results.html', {'track_results': search_result})
    else:
        form = SearchForm()
    return render(request, 'musics/search.html', {'form': form})

@login_required
def add_today_song(request, song_id):
    song = get_object_or_404(Song, pk=song_id)
    today_song = TodaySong.objects.create(
        song = song,
        user = request.user
    )
    today_song.save()
    song.add_num_mention()
    celery_save_user_activity.delay(request.user.id, 'set_today_song', song.id)

    return JsonResponse({'success': True})