from django.urls import path
from . import views

app_name = "user_messages"
urlpatterns = [
    path("send/", views.send_message, name="send_message"), # send messages
    path('inbox/', views.inbox, name = 'inbox'), # list messages
    path('<int:message_id>/', views.read_message, name = "read_message"), # read messages
]