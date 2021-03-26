from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class UserForm(UserCreationForm):
    # django.contrib.auth.forms 패키지의 UserCreationForm 클래스 상속
    email = forms.EmailField(label="이메일")
    
    class Meta:
        model = User
        fields = ("username", "email")