from django.contrib.auth import authenticate, login
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator
from django.db import IntegrityError
from django.shortcuts import render, get_object_or_404
from django.contrib import auth
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse_lazy

from .models import Ask, Answer, Account, AskLike, AnswerLike
from .forms import SignupForm, LoginForm, AskForm, AnswerForm
from django.views.generic import DetailView
from django.views.generic.edit import FormMixin
from taggit.models import Tag


def avatar(request):
    avatar = None
    try:
        if request.user.is_authenticated:
            avatar = Account.objects.get(user_id=request.user.id).user_avatar.url
    except ValueError:
        pass
    return avatar


def hot_tags(request):
    hot_tags = Ask.ask_tags.most_common()[:5]
    return render(request, 'asking/sidepanel.html', {'hot_tags': hot_tags})


def active_users(request):
    right_answers = Answer.objects.get(answer_is_right=True)
    for i in right_answers.count():
        Account.objects.get(user=i.answerer_name).user_rating += 1
    active = Account.objects.order_by('-user_rating')[:5]
    return render(request, 'asking/base.html', {'active': active})


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
        self.object = form.save()
        self.object.ask = self.get_object()
        self.object.answerer_name = self.request.user
        self.object.save()
        return super().form_valid(form)

    def get_success_url(self, **kwargs):
        return reverse_lazy('question', kwargs={'pk': self.get_object().id})


def signup(request):
    alert = False
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            try:
                user = User.objects.create_user(username=request.POST.get('username'), email=request.POST.get('email'),
                                                password=request.POST.get('password'))
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
    if request.method == 'POST':
        form = AskForm(request.POST)
        if form.is_valid():
            question = Ask.objects.create(ask_title=request.POST.get('ask_title'),
                                          ask_explane=request.POST.get('ask_explane'), asker_name=request.user)
            tags = request.POST.get('ask_tags').split(",")
            for tag in tags:
                tag = (str(tag)).replace(' ', '')
                question.ask_tags.add(tag)
            question.save()
            return HttpResponseRedirect('/{}/'.format(question.id))
        return render(request, 'asking/ask.html',
                      {'form': form, 'avatar': avatar(request), 'hot_tags': hot_tags, 'active_users': active_users})
    form = AskForm()
    return render(request, 'asking/ask.html',
                  {'form': form, 'avatar': avatar(request), 'hot_tags': hot_tags, 'active_users': active_users})


def index(request, flag=0, tag_slug=None):
    if flag == 0:
        index = Ask.objects.order_by('-ask_date')
        tag = None
        title = "Последние вопросы"
    else:
        index = Ask.objects.order_by('-ask_rating')
        tag = None
        title = "Популярные вопросы"
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        title = "Вопросы с тегом " + str(tag)
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
    # if request.method == 'POST':
    # 	form = SignupForm(request.POST)
    # 	if form.is_valid():
    # 		request.user.username = request.POST.get('username')
    # 		request.user.email = request.POST.get('username')
    # 		request.user.set_password(request.POST.get('password'))
    # 		request.user.account.user_avatar = request.FILES.get('user_avatar')
    # 		request.user.save()
    # 		request.user.account.save()
    # 		auth.authenticate(username=request.POST.get['username'], password=request.POST.get['password'])
    # 	return render(request, 'asking/settings.html', {'form': form, 'avatar': avatar(request)})
    # username = request.POST.get('username')
    # email = request.POST.get('username')
    # user_avatar = request.FILES.get('user_avatar')
    # form = SignupForm({'username': username, 'email': email, 'user_avatar': user_avatar})
    # return render(request, 'asking/settings.html', {'username': username, 'email': email, 'form': form, 'avatar': avatar(request)})
    pass


def asklikes(request, ask, like_dis):
    asklike = AskLike.objects.get(user=request.user, ask=ask)
    try:
        if not asklike or asklike.like == False and asklike.dislike == False:
            return False
    except ObjectDoesNotExist:
        if like_dis == 'asklike':
            if asklike.like == False:
                asklike.like = True
                asklike.dislike = False
            else:
                asklike.like = False
        else:
            if asklike.dislike == False:
                asklike.dislike = True
                asklike.like = False
            else:
                asklike.dislike = False
        asklike.save()
        ask.ask_rating = asklike.filter(like=True).count() - asklike.filter(dislike=True).count()
        ask.save()
        return True


def answerlikes(request, answer, like_dis):
    anslike = AnswerLike.objects.get(user=request.user, answer=answer)
    try:
        if not anslike or anslike.like == False and anslike.dislike == False:
            return False
    except ObjectDoesNotExist:
        if like_dis == 'anslike':
            if anslike.like == False:
                anslike.like = True
                anslike.dislike = False
            else:
                anslike.like = False
        else:
            if anslike.dislike == False:
                anslike.dislike = True
                anslike.like = False
            else:
                anslike.dislike = False
        anslike.save()
        return True


def add_asklike(request):
    if request.method == 'POST':
        ask = request.POST['ask_id']
        like_dis = request.POST['ask_like']
        likes_ask = AskLike.objects.filter(ask=ask, like=True).count()
        dis_ask = AskLike.objects.filter(ask=ask, dislike=True).count()
        if asklikes(request, ask, like_dis):
            likes_ask = AskLike.objects.filter(ask=ask, like=True).count()
            dis_ask = AskLike.objects.filter(ask=ask, dislike=True).count()
            return JsonResponse({'asklikes': likes_ask, 'askdislikes': dis_ask, 'ask_rating': ask.ask_rating})
        return JsonResponse({'asklikes': likes_ask, 'askdislikes': dis_ask, 'ask_rating': ask.ask_rating})


def add_anslike(request):
    if request.method == 'POST':
        answer = request.POST['ask_id']
        like_dis = request.POST['ask_like']
        likes_ans = AskLike.objects.filter(answer=answer, like=True).count()
        dis_ans = AskLike.objects.filter(answer=answer, dislike=True).count()
        if answerlikes(request, answer, like_dis):
            likes_ans = AskLike.objects.filter(answer=answer, like=True).count()
            dis_ans = AskLike.objects.filter(answer=answer, dislike=True).count()
            return JsonResponse({'anslikes': likes_ans, 'ansdislikes': dis_ans})
        return JsonResponse({'anslikes': likes_ans, 'ansdislikes': dis_ans})


def logout(request):
    if request.user.is_authenticated:
        auth.logout(request)
    return HttpResponseRedirect('/?continue=logout')
