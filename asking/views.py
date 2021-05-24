from django.db import IntegrityError
from django.shortcuts import render
from django.contrib import auth
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from .models import Ask, Answer, Account
from .forms import SignupForm, LoginForm, AskForm, AnswerForm


def login(request):
	return render(request, 'asking/login.html')


def signup(request):
	return render(request, 'asking/signup.html')


def signup_up(request):
	form = SignupForm()
	if request.method == 'POST':
		form = SignupForm(request.POST)
		if form.is_valid():
			try:
				user = User.objects.create_user(username=request.POST.get('user_login'), email=request.POST.get('user_email'), password=request.POST.get('user_password'))
				user.save()
				user_id = User.objects.get(id=user.pk)
				avatar = Account(user=user_id, avatar=request.POST.get('user_avatar'))
				avatar.save()
			except IntegrityError:
				return render(request, 'asking/signup.html', {'form': form})
			return HttpResponseRedirect('/?continue=login')
		return render(request, 'asking/signup.html', {'form': form})
	return render(request, 'asking/signup.html', {'form': form})

def ask(request):
	form = AskForm()
	if request.method == 'POST':
		form = AskForm(request.POST)
		if form.is_valid():
			question = Ask.objects.create(ask_title=request.POST.get('ask_title'), ask_explane=request.POST.get('ask_explane'), asker_name=request.user, ask_tags=request.POST.get('ask_tags'))
			question.save()
			return render(request, 'asking/index.html')
		return render(request, 'asking/ask.html', {'form': form})
	return render(request, 'asking/ask.html', {'form': form})

def index(request):
	index = Ask.objects.order_by('-ask_date')[:5]
	return render(request, 'asking/index.html', {'index': index})


def question(request):
	answer = Answer.objects.order_by('-answer_date')
	return render(request, 'asking/question.html')


def login_in(request):
	form = LoginForm()
	if request.method == 'POST':
		form = LoginForm(request.POST)
		if form.is_valid():
			user = auth.authenticate(username=request.POST.get('username'), password=request.POST.get('password'))
			if user is not None:
				auth.login(request, user)
				return HttpResponseRedirect('/?continue=index')
		return render(request, 'asking/login.html', {'form': form})
	return render(request, 'asking/login.html', {'form': form})


def logout(request):
	if request.user.is_authenticated:
		auth.logout(request)
	return HttpResponseRedirect('/?continue=logout')
# Create your views here.
