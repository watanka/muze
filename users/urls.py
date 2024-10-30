from django.urls import path
from . import views

app_name="users"
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("<int:pk>/", views.ProfileView.as_view(), name="profile"),
    # send song to other user
    # path('accounts/additional-info/', views.AdditionalInfoView.as_view(), name = 'additional_info')
]