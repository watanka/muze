from django.urls import path
from . import views

app_name="users"
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("<int:pk>/", views.DetailView.as_view(), name="detail"),
    path("login", views.login, name="login"),
    path("profile/", views.create_user_profile, name="create_user_profile")
    # send song to other user
]