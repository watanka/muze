"""
URL configuration for music_dashboard project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import render
from django.contrib import admin
from django.urls import include, path, reverse
from django.views.generic import TemplateView
from debug_toolbar.toolbar import debug_toolbar_urls

from musics.models import Song
from musics.views import SongListView

class HomeView(TemplateView):
    template_name = 'home.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        
        context['popular_song_list'] = Song.objects.all().order_by('-num_likes')[:10]
        context['new_release_song_list'] = Song.objects.all().order_by('-release_date')[:10]

        return context

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('messages/', include("user_messages.urls")),
    path('users/', include("users.urls")),
    path('musics/', include("musics.urls")),
    path('polls/', include("polls.urls")),
    path("admin/", admin.site.urls),
    path("accounts/", include("allauth.urls")),
    path('', include('django_prometheus.urls'))
] + debug_toolbar_urls() \
+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) \
+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)