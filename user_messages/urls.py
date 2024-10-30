from django.urls import path
from . import views

app_name = "user_messages"
urlpatterns = [
    path("<int:song_id>/send", views.send_message, name="send_message"), # send messages
    path('inbox/', views.inbox, name = 'inbox'), # list messages
    path('<int:message_id>/', views.read_message, name = "read_message"), # read messages
    path('unread_messages_count/', views.unread, name="unread_messages_count")
]