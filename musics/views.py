from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.urls import reverse
from django.views.generic import ListView, DetailView, View
from django.shortcuts import render, get_object_or_404, redirect
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

def detail(request, song_id):
    song = get_object_or_404(Song, id = song_id)
    comments = song.comments.all()
    context = {
        'song': song,
        'comments': comments
    }
    return render(request, 'musics/detail.html', context)

class CommentView(View):
    def get(self, request, song_id):
        song = get_object_or_404(Song, id=song_id)
        comments = song.comments.all()  # song에 연결된 댓글 가져오기
        return render(request, "musics/comments.html", {'song': song, 'comments': comments})

    def post(self, request, song_id):
        song = get_object_or_404(Song, id=song_id)
        form = CommentForm(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.song = song
            new_comment.save()
            return redirect('musics:comments', song_id=song_id)
        # 유효하지 않은 폼일 경우 댓글 목록과 함께 다시 렌더링
        comments = song.comments.all()
        return redirect(reverse('musics:detail', args=(song.id,)))
    
    # render(request, "musics/comments.html", {'song': song, 'comments': comments, 'form': form})
    
    def get_queryset(self):
        song_id =self.kwargs['song_id']
        return Comment.objects.filter(song__id=song_id).order_by('-created_at')  # 특정 Song에 연결된 댓글만 가져옴

def add_comment(request, song_id):
    song = get_object_or_404(Song, id = song_id)
    # validation
    Comment.objects.create(
        song = song,
        content = request.content
    )

def likes(request, song_id):
    pass