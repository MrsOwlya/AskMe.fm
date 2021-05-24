from django.forms import Textarea

from .models import Account, Ask, Answer
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.core import validators
from django import forms
from django.contrib.auth.models import User
import re

class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите логин'
            }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите пароль'
            }))

    def clean(self):
        login = self.cleaned_data['username']
        password = self.cleaned_data['password']
        if not User.objects.filter(username=login).exists():
            raise forms.ValidationError(f'Пользователь с логином {login} не найден')
        user = User.objects.filter(username=login).first()
        if user:
            if not user.check_password(password):
                raise forms.ValidationError('Неверный пароль')
        return self.cleaned_data


    class Meta:
        model = User
        fields = ['username', 'password']

class SignupForm(forms.Form):
    user_login = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Введите логин'
    }))
    user_email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Введите email'
    }))
    user_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Введите пароль'
    }))
    user_password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Повторите пароль'
    }))
    user_avatar = forms.ImageField(widget=forms.FileInput(attrs={
        'class': 'form-control',
        'placeholder': 'Загрузите аватарку'
    }))

    def clean(self):
        user_login = self.cleaned_data['user_login']
        user_email = self.cleaned_data['user_email']
        user_password = self.cleaned_data['user_password']
        user_password2 = self.cleaned_data['user_password2']
        if not user_login or len(user_login) == 0:
            raise forms.ValidationError("Введите логин!")
        if not user_email or len(user_email) == 0:
            raise forms.ValidationError("Введите email!")
        if user_password != user_password2:
            raise forms.ValidationError("Пароли не совпадают!")
        return self.cleaned_data

    class Meta:
        model = Account
        fields = ['username', 'email', 'password', 'user_avatar']

class AskForm(forms.ModelForm):
    ask_title = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Вопрос'
    }))
    ask_explane = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'form-control',
        'placeholder': 'Пояснение'
    }))
    ask_tags = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Теги'
    }))

    def clean(self):
        ask_title = self.cleaned_data['ask_title']
        ask_explane = self.cleaned_data['ask_explane']
        ask_tags = self.cleaned_data['ask_tags']
        if not ask_title or len(ask_title) == 0:
            raise forms.ValidationError("Введите вопрос!")
        if not ask_explane or len(ask_explane) == 0:
            raise forms.ValidationError("Введите пояснение!")
        if not ask_tags or len(ask_tags) == 0:
            raise forms.ValidationError("Введите теги!")
        return self.cleaned_data

    class Meta:
        model = Ask
        fields = ['ask_title', 'ask_explane', 'ask_tags']

class AnswerForm(forms.ModelForm):
    answer_text = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'form-control',
        'rows': 4,
        'placeholder': 'Ваш ответ'
    }))

    def clean(self):
        answer_text = self.cleaned_data['answer_text']
        if not answer_text or len(answer_text) == 0:
            raise forms.ValidationError("Введите ответ!")
        return self.cleaned_data

    class Meta:
        model = Answer
        fields = ['answer_text']
