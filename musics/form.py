from django import forms
from .models import Song, Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']

class SearchForm(forms.Form):
    CATEGORY_CHOICES = [
        ('artist', '가수'),
        ('title', '곡 이름')
    ] # track만 동작. 나머지 category는 구현X

    category = forms.ChoiceField(
        choices=CATEGORY_CHOICES,
        widget = forms.Select(attrs={
            'class': 'form-control',
            'style': 'max-height: 200px; overflow-y: auto;'
        }),
        label = '카테고리 선택'
    )
    keyword = forms.CharField(widget = forms.Textarea(
        attrs = {
            'class': 'form-control', 
            'rows': 4,
            'placeholder': '검색할 키워드를 입력하세요.'
        }),
        label = '키워드 입력'
    ) # 결과가 안 나올 경우 표시해줘야함.