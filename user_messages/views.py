from django.apps import apps
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import Message
from .forms import MessageForm
from music_dashboard.tasks import celery_save_user_activity

import logging
logger = logging.getLogger('user_message')

Song = apps.get_model('musics', 'Song')

@login_required
def send_message(request, song_id): 
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            selected_song = get_object_or_404(Song, id=song_id)
            selected_song.add_num_mention()

            receiver = form.clean_data['receiver']
            content = form.clean_data['content']

            message = Message.objects.save_message(request.user, receiver, selected_song, content)
            
            logger.info(f"Message sent by {request.user.username} to {receiver}: song {selected_song.title}")
            
            celery_save_user_activity.delay(user = request.user,
                                            activity_type = 'message',
                                            song = selected_song,
                                            friend_user = receiver)
            return redirect(reverse('musics:detail', args=(song_id, )))
    else:
        form = MessageForm()
    return render(request, 'user_messages/send_message.html', {'form': form})

@login_required
def unread(request):
    unread = Message.objects.get_unread_messages(user=request.user)
    return JsonResponse({'unread_messages_count': len(unread)})

@login_required
def inbox(request):
    messages = Message.objects.list_inbox(receiver=request.user)
    return render(request, 'user_messages/inbox.html', {'messages': messages})

@login_required
def read_message(request, message_id): 
    message = Message.objects.get(id = message_id, receiver = request.user)
    message.read_message()

    logger.info(f"User {request.user.username} read message {message_id}")
    return render(request, 'user_messages/read_message.html', {'message': message})