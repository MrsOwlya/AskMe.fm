from django.contrib.auth import authenticate, login
from django.core.paginator import Paginator
from django.db import IntegrityError
from django.shortcuts import render, get_object_or_404
from django.contrib import auth
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views import View

from .models import Ask, Answer, Account
from .forms import SignupForm, LoginForm, AskForm, AnswerForm
from django.views.generic import DetailView
from django.views.generic.edit import FormMixin, CreateView
from taggit.models import Tag


def avatar(request):
	avatar = None
	try:
		if request.user.is_authenticated:
			avatar=Account.objects.get(user_id=request.user.id).user_avatar.url
	except ValueError:
		pass
	return avatar

def hot_tags(request):
	hot_tags = Ask.ask_tags.most_common()[:5]
	return render(request, 'asking/sidepanel.html', {'hot_tags': hot_tags})

def active_users(request):
	active_users = Account.objects.order_by('-user_rating')[:5]
	return render(request, 'asking/base.html', {'active_users': active_users})

class QuestDetailView(FormMixin, DetailView):
	model = Ask
	template_name = 'asking/question.html'
	context_object_name = 'quest'
	form_class = AnswerForm

	def get(self, request, *args, **kwargs):
		self.object = self.get_object()
		self.object.ask_rating += 1
		self.object.save()
		context = self.get_context_data(object=self.object)
		return self.render_to_response(context)

	def post(self, request, *args, **kwargs):
		form = self.get_form()
		if form.is_valid():
			active = Account.objects.get(user=request.user)
			active.user_rating += 1
			active.save()
			return self.form_valid(form)
		else:
			return self.form_invalid(form)

	def form_valid(self, form):
		self.object=form.save()
		self.object.ask=self.get_object()
		self.object.answerer_name=self.request.user
		self.object.save()
		return super().form_valid(form)

	def get_success_url(self, **kwargs):
		return reverse_lazy('question', kwargs={'pk':self.get_object().id})

def signup(request):
	alert = False
	if request.method == "POST":
		form = SignupForm(request.POST)
		if form.is_valid():
			try:
				user = User.objects.create_user(username=request.POST.get('username'), email=request.POST.get('email'), password=request.POST.get('password'))
				user.save()
				user_pk = User.objects.get(id=user.pk)
				user_avatar = Account(user=user_pk, user_avatar=request.POST.get('user_avatar'))
				user_avatar.save()
			except IntegrityError:
				alert = False
				return render(request, 'asking/signup.html', {'form': form, 'alert': alert})
		alert = True
		return render(request, 'asking/signup.html', {'form': form, 'alert': alert})
	form = SignupForm()
	return render(request, 'asking/signup.html', {'form': form, 'alert': alert})

def ask(request):
	form = AskForm()
	if request.method == 'POST':
		form = AskForm(request.POST)
		if form.is_valid():
			question = Ask.objects.create(ask_title=request.POST.get('ask_title'), ask_explane=request.POST.get('ask_explane'), asker_name=request.user)
			tags = request.POST.get('ask_tags').split(",")
			for tag in tags:
				tag = (str(tag)).replace(' ', '')
				question.ask_tags.add(tag)
			question.save()
			active = Account.objects.get(user=request.user)
			active.user_rating += 1
			active.save()
			return render(request, 'asking/index.html')
		return render(request, 'asking/ask.html', {'form': form, 'avatar': avatar(request), 'hot_tags': hot_tags, 'active_users': active_users})
	return render(request, 'asking/ask.html', {'form': form, 'avatar': avatar(request), 'hot_tags': hot_tags, 'active_users': active_users})

def index(request, flag=0, tag_slug=None):
	if flag==0:
		index = Ask.objects.order_by('-ask_date')
		tag = None
		title = "Последние вопросы"
	else:
		index = Ask.objects.order_by('-ask_rating')
		tag = None
		title = "Популярные вопросы"
	if tag_slug:
		tag = get_object_or_404(Tag, slug=tag_slug)
		title = "Вопросы с тегом "+str(tag)
		index = index.filter(ask_tags__in=[tag])
	paginator = Paginator(index, 3)
	page_number = request.GET.get('page')
	page_obj = paginator.get_page(page_number)
	return render(request, 'asking/index.html',
					  {'index': index, 'title': title, 'tag': tag, 'avatar': avatar(request), 'hot_tags': hot_tags, \
					   'active_users': active_users, 'page_obj': page_obj})


def index_hot(request):
	return index(request, 1)


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

def settings(request):

	return render(request, 'asking/settings.html', {'avatar': avatar(request)})

def logout(request):
	if request.user.is_authenticated:
		auth.logout(request)
	return HttpResponseRedirect('/?continue=logout')
