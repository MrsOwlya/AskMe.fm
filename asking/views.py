from django.db import IntegrityError
from django.shortcuts import render, get_object_or_404
from django.contrib import auth
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from .models import Ask, Answer, Account
from .forms import SignupForm, LoginForm, AskForm, AnswerForm
from django.views.generic import DetailView
from django.views.generic.edit import FormMixin, CreateView
from taggit.models import Tag


def hot_tags(request):
	hot_tags = Ask.ask_tags.most_common()[:3]
	return render(request, 'asking/tags.html', {'hot_tags': hot_tags})

class QuestDetailView(FormMixin, DetailView):
	model = Ask
	template_name = 'asking/question.html'
	context_object_name = 'quest'
	form_class = AnswerForm

	def post(self, request, *args, **kwargs):
		form = self.get_form()
		if form.is_valid():
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

class SignupView(CreateView):
	model = Account
	template_name = 'asking/signup.html'
	form_class = SignupForm
	success_url = 'asking/login.html'

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
			return render(request, 'asking/index.html')
		return render(request, 'asking/ask.html', {'form': form, 'avatar': avatar(request), 'hot_tags': hot_tags})
	return render(request, 'asking/ask.html', {'form': form, 'avatar': avatar(request), 'hot_tags': hot_tags})

def index(request, flag=0, tag_slug=None):
	if flag==0:
		index = Ask.objects.order_by('-ask_date')
		tag = None
		title = "Последние ворпосы"
		if tag_slug:
			tag=get_object_or_404(Tag, slug=tag_slug)
			index = index.filter(ask_tags__in=[tag])
			return render(request, 'asking/index.html', {'index': index, 'title': title, 'tag': tag, 'avatar': avatar(request), 'hot_tags': hot_tags})
		return render(request, 'asking/index.html', {'index': index, 'title': title, 'tag': tag, 'avatar': avatar(request), 'hot_tags': hot_tags})
	else:
		index = Ask.objects.order_by('-ask_rating')
		tag = None
		title = "Популярные ворпосы"
		if tag_slug:
			tag = get_object_or_404(Tag, slug=tag_slug)
			index = index.filter(ask_tags__in=[tag])
			return render(request, 'asking/index.html',
						  {'index': index, 'title': title, 'tag': tag, 'avatar': avatar(request), 'hot_tags': hot_tags})
		return render(request, 'asking/index.html',
					  {'index': index, 'title': title, 'tag': tag, 'avatar': avatar(request), 'hot_tags': hot_tags})


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

def avatar(request):
	avatar = None
	try:
		if request.user.is_authenticated:
			avatar=Account.objects.get(user_id=request.user.id).user_avatar.url
	except ValueError:
		pass
	return avatar