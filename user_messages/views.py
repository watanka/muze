from django.apps import apps
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import Message
from .forms import MessageForm
# Create your views here.

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

            return redirect(reverse('musics:detail', args=(song_id, )))
    else:
        form = MessageForm()
    return render(request, 'user_messages/send_message.html', {'form': form})

@login_required
def inbox(request):
    messages = Message.objects.filter(receiver=request.user).order_by('-timestamp')
    return render(request, 'user_messages/inbox.html', {'messages': messages})

@login_required
def read_message(request, message_id): 
    message = Message.objects.get(id = message_id, receiver = request.user)
    message.is_read = True
    message.save()
    return render(request, 'user_messages/read_message.html', {'message': message})