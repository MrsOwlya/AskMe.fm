from datetime import timezone, datetime
from taggit.forms import TagField, TagWidget
from django.forms import Textarea
from .models import Account, Ask, Answer
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.core import validators
from django import forms
from django.contrib.auth.models import User
import re

class LoginForm(forms.ModelForm):
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

class SignupForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Введите логин'
    }))
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Введите email'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Введите пароль'
    }))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Повторите пароль'
    }))
    user_avatar = forms.ImageField(required=False, widget=forms.FileInput(attrs={
        'class': 'form-control',
        'placeholder': 'Загрузите аватарку'
    }))

    def clean(self):
        username = self.cleaned_data['username']
        email = self.cleaned_data['email']
        password = self.cleaned_data['password']
        password2 = self.cleaned_data['password2']
        if not username or len(username) == 0:
            raise forms.ValidationError("Введите логин!")
        if len(username) <=3 or len(username) >= 20:
            raise forms.ValidationError("Некорректный логин!")
        if not email or len(email) == 0:
            raise forms.ValidationError("Введите email!")
        if User.objects.filter(email=email).exists() and not User.objects.filter(username=username, email=email).exists():
            raise forms.ValidationError("Пользователь с таким email уже зарегистрирован!")
        if not User.objects.filter(username=username, email=email).exists():
            if len(password) == 0:
                raise forms.ValidationError("Введите пароль!")
            if len(password2) == 0:
                raise forms.ValidationError("Повторите пароль!")
            if len(password) <= 8:
                raise forms.ValidationError("Пароль слишком короткий!")
            if password != password2:
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
    ask_tags = TagField(widget=TagWidget(attrs={
        'class': 'form-control',
        'placeholder': 'Теги (введите через запятую)'
    }))

    def clean(self):
        ask_title = self.cleaned_data['ask_title']
        ask_explane = self.cleaned_data['ask_explane']
        ask_tags = self.cleaned_data['ask_tags']
        early_quest = Ask.objects.all()
        if not ask_title or len(ask_title) == 0:
            raise forms.ValidationError("Введите вопрос!")
        if len(ask_title) >= 80:
            raise forms.ValidationError("Слишком длинный ворпос!")
        if not ask_explane or len(ask_explane) == 0:
            raise forms.ValidationError("Введите пояснение!")
        if not ask_tags or len(ask_tags) == 0:
            raise forms.ValidationError("Введите теги!")
        count = 0
        for tag in ask_tags:
            count = count + 1
        if count > 3:
            raise forms.ValidationError("Введите не более трех тегов!")
        for e in early_quest:
            if ask_title == e.ask_title and ask_explane == e.ask_explane and ask_tags == e.ask_tags:
                raise ValidationError("Такой вопрос уже существует!")
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
        if len(answer_text) >= 500:
            raise forms.ValidationError("Слишком длинный ответ!")
        return self.cleaned_data

    class Meta:
        model = Answer
        fields = ['answer_text']
