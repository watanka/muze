from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login

from .models import UserProfile
from .forms import UserProfileForm
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

def create_user_profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES)  # 파일 업로드를 위해 request.FILES 사용
        if form.is_valid():
            user_profile = form.save(commit=False)
            user_profile.user = request.user  # 현재 로그인한 사용자와 연결
            user_profile.save()
            return redirect('/')  # 프로필 생성 후 리디렉션할 URL
    else:
        form = UserProfileForm()

    return render(request, 'users/profile.html', {'form': form})  # 템플릿에 폼 전달