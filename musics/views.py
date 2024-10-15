from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.urls import reverse
from django.views.generic import ListView, DetailView, View
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .models import Song, Comment
from .form import CommentForm

class SongListView(ListView):
    model = Song
    template_name = "musics/index.html"
    context_object_name = "song_list"
    paginate_by=20
    

class SongDetailView(DetailView):
    model = Song
    template_name = "musics/detail.html"
    context_object_name = "song"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

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
    
    user_profile = request.user.userprofile
    if song in user_profile.liked_songs.all():
        # 유저가 이미 이 곡을 좋아요 했을 경우
        return redirect(reverse('musics:detail', args=[song_id]))

    song.num_likes += 1
    song.save(update_fields=['num_likes'])
    user_profile.liked_songs.add(song)

    return redirect(reverse('musics:detail', args=(song_id,)))
