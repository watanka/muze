from django.urls import path
from . import views

app_name="musics"
urlpatterns = [
    path("", views.index, name="index"),
    path("<int:song_id>/", views.detail, name="detail"),
    path("<int:song_id>/comments/", views.comments, name="comments"),
    path("<int:question_id>/likes/", views.likes, name="likes")
]