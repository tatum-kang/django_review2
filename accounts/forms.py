from django.forms import forms
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth import get_user_model  # 현재 활성화(active)된 user model을 return하는 함수


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = get_user_model()
        fields = ['email', 'first_name', 'last_name', ]