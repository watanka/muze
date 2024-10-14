from django.urls import path
from . import views

app_name="users"
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("<int:pk>/", views.DetailView.as_view(), name="detail"),
    path("login", views.login, name="login")
    # send song to other user
]