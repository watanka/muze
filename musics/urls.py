from django.urls import path
from . import views

app_name="musics"
urlpatterns = [
    path("", views.index, name="index"),
    path("<int:pk>/", views.SongDetailView.as_view(), name="detail"),
    path("<int:song_id>/comments/", views.CommentView.as_view(), name="comments"),

    path("<int:question_id>/likes/", views.likes, name="likes")
]