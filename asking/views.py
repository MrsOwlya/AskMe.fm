from django.db import IntegrityError
from django.shortcuts import render
from django.contrib import auth
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from .models import Ask, Answer, Account
from .forms import SignupForm, LoginForm, AskForm, AnswerForm
from django.views.generic import DetailView


def signup_up(request):
	form = SignupForm()
	if request.method == 'POST':
		form = SignupForm(request.POST)
		if form.is_valid():
			try:
				user = User.objects.create_user(username=request.POST.get('user_login'), email=request.POST.get('user_email'), password=request.POST.get('user_password'))
				user.save()
				user_id = User.objects.get(id=user.pk)
				avatar = Account(user=user_id, user_avatar=request.POST.get('user_avatar'))
				avatar.save()
			except IntegrityError:
				return render(request, 'asking/signup.html', {'form': form})
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
		return render(request, 'asking/ask.html', {'form': form, 'avatar': avatar(request)})
	return render(request, 'asking/ask.html', {'form': form, 'avatar': avatar(request)})

def index(request):
	index = Ask.objects.order_by('-ask_date')[:5]
	return render(request, 'asking/index.html', {'index': index, 'avatar': avatar(request)})

class QuestDetailView(DetailView):
	model = Ask
	template_name = 'asking/question.html'
	context_object_name = 'quest'


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

def avatar(request):
	avatar = None
	try:
		if request.user.is_authenticated:
			avatar=Account.objects.get(user_id=request.user.id).user_avatar.url
	except ValueError:
		pass
	return avatar

# Create your views here.
