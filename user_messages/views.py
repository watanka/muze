from django.apps import apps
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import Message
from .forms import MessageForm

import logging
logger = logging.getLogger('user_message')

Song = apps.get_model('musics', 'Song')

@login_required
def send_message(request, song_id): 
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            selected_song = get_object_or_404(Song, id=song_id)
            selected_song.num_mention += 1
            selected_song.save(update_fields=['num_mention'])

            message = form.save(commit=False)
            message.sender = request.user
            message.song_id = song_id
            message.save()
            
            logger.info(f"Message sent by {request.user.username} to {request.POST.get('receiver')}: song {selected_song.title}")
            
            return redirect(reverse('musics:detail', args=(song_id, )))
    else:
        form = MessageForm()
    return render(request, 'user_messages/send_message.html', {'form': form})

@login_required
def unread(request):
    unread = Message.objects.filter(receiver=request.user).filter(is_read=False)
    return JsonResponse({'unread_messages_count': len(unread)})

@login_required
def inbox(request):
    messages = Message.objects.filter(receiver=request.user).order_by('-timestamp')

    return render(request, 'user_messages/inbox.html', {'messages': messages})

@login_required
def read_message(request, message_id): 
    message = Message.objects.get(id = message_id, receiver = request.user)
    message.is_read = True
    message.save()

    logger.info(f"User {request.user.username} read message {message_id}")
    return render(request, 'user_messages/read_message.html', {'message': message})