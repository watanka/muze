from allauth.account.forms import SignupForm
from django import forms
from .models import User

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['nickname', 'profile_picture']  # 사용자에게 입력받을 필드 목록


class MyCustomSignupForm(SignupForm):
    # 추가 필드 정의
    nickname = forms.CharField(max_length=20, label='Nickname')
    profile_picture = forms.ImageField(required=False)
    def save(self, request):
        # 부모 클래스의 save 호출하여 User 객체 생성
        user = super(MyCustomSignupForm, self).save(request)
        user.nickname = self.cleaned_data['nickname']
        if self.cleaned_data['profile_picture']:
            user.profile_picture = self.cleaned_data['profile_picture']
        user.save()
        return user