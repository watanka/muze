from django.shortcuts import render, get_object_or_404
from django.views import generic, View
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse

from django.dispatch import receiver
from allauth.account.signals import (user_logged_in,
                                     user_logged_out, 
                                     user_signed_up,
                                     email_confirmed,
                                     password_changed)
from allauth.socialaccount.signals import pre_social_login

from .models import User, FriendRequest, UserActivity
import logging

logger = logging.getLogger('allauth')


class IndexView(generic.ListView):
    model = User
    template_name = "users/index.html"
    context_object_name = "user_list"


class ProfileView(generic.DetailView):
    model = User
    template_name = "users/profile.html"

@login_required
def friend_request(request, receiver_id):
    sender_id = request.POST.get('sender_id')
    login_user = request.user
    if request.method == 'POST':
        receiver = User.objects.get(id=receiver_id)
        if receiver in login_user.friends.all():
            return JsonResponse({'error': '이미 친구입니다.'}, status = 400)
        else:
            friend_request = FriendRequest.objects.filter(from_user=login_user, to_user=receiver)

            if len(friend_request) >= 1:
                return JsonResponse({'error': '친구 요청을 이미 보냈습니다.'})
            else: 
                FriendRequest.objects.create(
                    from_user = login_user,
                    to_user = receiver
                )
                return JsonResponse({'message': '친구 요청을 보냈습니다.'})
                
@login_required
def accept_friend_request(request):       
    friend_request = get_object_or_404(FriendRequest, 
                                       from_user = request.POST.get('sender_id'), 
                                       to_user = request.POST.get('receiver_id'))
    if friend_request.to_user != request.user:
        raise PermissionDenied("권한이 없습니다.")

    sender_id = friend_request.from_user.id
    sender = get_object_or_404(User, pk=sender_id)
    
    request.user.friends.add(sender)
    sender.friends.add(request.user)
    
    friend_request.delete()
    
    return JsonResponse({'message': f'{sender.nickname}과(와) 친구가 되었습니다.'})
                
@login_required
def reject_friend_request(request):       
    friend_request = get_object_or_404(FriendRequest, 
                                       from_user = request.POST.get('sender_id'), 
                                       to_user = request.POST.get('receiver_id'))
    if friend_request.to_user != request.user:
        raise PermissionDenied("권한이 없습니다.")

    sender = friend_request.from_user
    friend_request.delete()
    return JsonResponse({'message': f'{sender.nickname}의 친구요청을 거절하였습니다.'})

@method_decorator(login_required, name='dispatch')
class FriendRequestView(generic.ListView):
    model = FriendRequest
    template_name = "users/friend_request_list.html"
    context_object_name = 'friend_requests'  # context 이름 지정

    def get_queryset(self):
        receiver_id = self.kwargs.get('receiver_id')
        return FriendRequest.objects.filter(receiver_id=receiver_id)


class FeedView(LoginRequiredMixin, generic.ListView):
    model = UserActivity
    template_name = 'users/feed.html'
    context_object_name = 'feeds'

    def get_queryset(self):
        user = self.request.user

        return UserActivity.objects.filter(user__in = user.friends.all()).order_by('-created_at')





def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

@receiver(pre_social_login)
def log_social_account_signup(request, sociallogin, **kwargs):
    user = sociallogin.user
    provider = sociallogin.account.provider
    logger.info(f"Social account signup for user: {user.username}, Provider: {provider}")

@receiver(user_logged_in)
def log_user_logged_in(request, user, **kwargs):
    logger.info(f'User logged in: {user.username}, IP: {get_client_ip(request)}')

@receiver(user_logged_out)
def log_user_logged_out(request, user, **kwargs):
    logger.info(f'User logged out: {user.username}, IP: {get_client_ip(request)}')

@receiver(user_signed_up)
def log_user_signed_up(request, user, **kwargs):
    logger.info(f'User signed up: {user.username}, Email: {user.email}')


@receiver(email_confirmed)
def log_email_confirmed(request, email_address, **kwargs):
    logger.info(f"Email confirmed for: {email_address.user.username}, Email: {email_address.email}")

@receiver(password_changed)
def log_password_changed(request, user, **kwargs):
    logger.info(f"Password changed for: {user.username}")


def check_nickname(request):
    if request.method == 'GET':
        nickname = request.GET.get('nickname', None)
        exists = User.objects.filter(nickname=nickname).exists()
        return JsonResponse({'duplicate': exists})
    return JsonResponse({'duplicate': False})

# def signin(request):
#     username = request.POST['username']
#     password = request.POST['password']
#     user = authenticate(request, username=username, password=password)
#     if user is not None:
#         login(request, user)
#         # TODO: redirect to home page.
#     else:
#         # Return an invalid login' error message
#         return render(request, 'users/login_error.html')




# class AdditionalInfoView(View):
#     def get(self, request):
#         form = AdditionalInfoForm()
#         return render(request, 'users/additional_info.html', {'form': form})

#     def post(self, request):
#         form = AdditionalInfoForm(request.POST)
#         if form.is_valid():
#             profile = User(user=request.user, **form.cleaned_data)
#             profile.save()
#             return redirect('home')  # 홈으로 리다이렉트
#         return render(request, 'users/additional_info.html', {'form': form})
