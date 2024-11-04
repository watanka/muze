from django.urls import path
from . import views

app_name="musics"
urlpatterns = [
    path("", views.SongListView.as_view(), name="index"),
    path("<int:pk>/", views.SongDetailView.as_view(), name="detail"),
    path("<int:song_id>/comments/", views.CommentView.as_view(), name="comments"),
    path("<int:song_id>/like/", views.likes, name="like"),
    path("search", views.search_view, name="search"),
    path("request_song", views.request_song, name="request_song"),
    path("add_today_song", views.add_today_song, name="add_today_song"),
]