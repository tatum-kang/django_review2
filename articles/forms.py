from django import forms
from .models import Article, Comment

class ArticleForm(forms.ModelForm):

    class Meta:
        model = Article
        fields = ['title', 'content', ]


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        # fields = '__all__' 
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'cols': 80, 'rows': 1}),
        }
