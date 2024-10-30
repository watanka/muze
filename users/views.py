from django.shortcuts import render, get_object_or_404
from django.views import generic, View
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login

from django.dispatch import receiver
from allauth.account.signals import (user_logged_in,
                                     user_logged_out, 
                                     user_signed_up,
                                     email_confirmed,
                                     password_changed)
from allauth.socialaccount.signals import pre_social_login

from .models import User
from .forms import AdditionalInfoForm
import logging

logger = logging.getLogger('allauth')


class IndexView(generic.ListView):
    model = User
    template_name = "users/index.html"
    context_object_name = "user_list"


class ProfileView(generic.DetailView):
    model = User
    template_name = "users/profile.html"

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
