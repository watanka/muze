from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import Message
from .forms import MessageForm
# Create your views here.

@login_required
def send_message(request): 
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.save()
            return redirect(reverse('user_messages:inbox'))
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