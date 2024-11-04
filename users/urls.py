from django.urls import path
from . import views

app_name="users"
urlpatterns = [
    # path("", views.IndexView.as_view(), name="index"),
    path("", views.FeedView.as_view(), name="newsfeed"),
    path("<int:pk>/profile", views.ProfileView.as_view(), name="profile"),
    path("<int:receiver_id>/friend_request", views.friend_request, name="friend_request"),
    path("friend_request/accept", views.accept_friend_request, name="accept_friend_request"),
    path("friend_request/reject", views.reject_friend_request, name="reject_friend_request"),
    path("<int:receiver_id>/friend_request_list", views.FriendRequestView.as_view(), name="friend_request_list"),
    path("check_nickname", views.check_nickname, name="check_nickname"),
    
    # send song to other user
    # path('accounts/additional-info/', views.AdditionalInfoView.as_view(), name = 'additional_info')
]