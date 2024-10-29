from django.shortcuts import render, get_object_or_404
from django.views import generic, View
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login

from .models import User
from .forms import AdditionalInfoForm
# Create your views here.

class IndexView(generic.ListView):
    model = User
    template_name = "users/index.html"
    context_object_name = "user_list"


class ProfileView(generic.DetailView):
    model = User
    template_name = "users/profile.html"
    
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

class AdditionalInfoView(View):
    def get(self, request):
        form = AdditionalInfoForm()
        return render(request, 'users/additional_info.html', {'form': form})

    def post(self, request):
        form = AdditionalInfoForm(request.POST)
        if form.is_valid():
            profile = User(user=request.user, **form.cleaned_data)
            profile.save()
            return redirect('home')  # 홈으로 리다이렉트
        return render(request, 'users/additional_info.html', {'form': form})
