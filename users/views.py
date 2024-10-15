from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from .models import UserProfile
# Create your views here.

class IndexView(generic.ListView):
    model = UserProfile
    template_name = "users/index.html"
    context_object_name = "user_list"


class DetailView(generic.DetailView):
    model = UserProfile
    template_name = "users/detail.html"
    
def signup(request):
    pass

def signin(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        # TODO: redirect to home page.
    else:
        # Return an invalid login' error message
        return render(request, 'users/login_error.html')
