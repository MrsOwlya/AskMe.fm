from collections import OrderedDict
from itertools import chain
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator
from django.db import IntegrityError
from django.db.models import Count, Subquery
from django.shortcuts import render, get_object_or_404
from django.contrib import auth
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.list import MultipleObjectMixin

from .models import Ask, Answer, Account, AskLike, AnswerLike
from .forms import SignupForm, LoginForm, AskForm, AnswerForm
from django.views.generic import DetailView, UpdateView, DeleteView, ListView
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
    hot_list = []
    for a in hot_tags:
        hott = {}
        b = a.slug
        c = a.name
        hott[b] = c
        hot_list.append(hott)
    return JsonResponse(hot_list, safe=False)

def active_users(request):
    right_answers = Answer.objects.all().filter(answer_is_right=True)
    for i in right_answers:
        Account.objects.get(user=i.answerer_name).user_rating += 1
        Account.objects.get(user=i.answerer_name).save()
    active = Account.objects.order_by('-user_rating')[:5]
    actus = []
    for a in active:
        b = a.user
        c = b.username
        actus.append(c)
    return JsonResponse(actus, safe=False)

class QuestDetailView(FormMixin, DetailView, MultipleObjectMixin):
    model = Ask
    template_name = 'asking/question.html'
    context_object_name = 'quest'
    form_class = AnswerForm
    paginate_by = 2

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

    def get_context_data(self, **kwargs):
        object_list = Answer.objects.filter(ask=self.get_object()).order_by('-answer_date')
        context = super(QuestDetailView, self).get_context_data(object_list=object_list, **kwargs)
        try:
            context['avatar'] = Account.objects.get(user=self.request.user).user_avatar.url
        except:
            pass
        return context

class QuestUpdateView(UpdateView):
    model = Ask
    template_name = 'asking/ask.html'

    form_class = AskForm

    def get_context_data(self, **kwargs):
        context = super(QuestUpdateView, self).get_context_data(**kwargs)
        try:
            context['avatar'] = Account.objects.get(user=self.request.user).user_avatar.url
        except:
            pass
        return context

class QuestDeleteView(DeleteView):
    model = Ask
    template_name = 'asking/question.html'
    success_url = '/hot/'

class QuestSearchView(ListView):
    model = Ask
    paginate_by = 3
    template_name = 'asking/search.html'

    def get_queryset(self):
        search_set = []
        quest = (str(self.request.GET.get("q"))).split(" ")
        for q in quest:
            q = (str(q)).replace(' ','')
            search_set.append(Ask.objects.filter(ask_title__icontains=q))
            tags = Tag.objects.filter(name__icontains=q)
            for tag in tags:
                search_set.append(Ask.objects.filter(ask_tags=tag))
            search_set.append(Ask.objects.filter(ask_explane__icontains=q))
        same_list = []
        for s in search_set:
            same_list2 = {}
            count = 0
            for same in search_set:
                if set(s) == set(same):
                    count += 1
                    if count >= 1:
                        search_set.remove(same)
            same_list2['count'] = count
            same_list2['value'] = s
            same_list.append(same_list2)
        same_list.sort(key = lambda d: d['count'], reverse=True)
        fin = []
        for q in same_list:
            fin.append(q['value'])
        final = list(chain(*fin))
        if not final:
            self.search = False
        else:
            self.search = True
        return final

    def get_context_data(self, *args, **kwargs):
        context = super(QuestSearchView, self).get_context_data(*args, **kwargs)
        context['q'] = self.request.GET.get("q")
        if self.search == True:
            context['title'] = "Результаты поиска: " + context['q']
        else:
            context['title'] = "По вашему запросу ничего не нашлось :("
        try:
            context['avatar'] = Account.objects.get(user=self.request.user).user_avatar.url
        except:
            pass
        return context

class AnsUpdateView(UpdateView):
    model = Answer
    template_name = 'asking/answer_form.html'

    form_class = AnswerForm

    def get_context_data(self, **kwargs):
        context = super(AnsUpdateView, self).get_context_data(**kwargs)
        try:
            context['avatar'] = Account.objects.get(user=self.request.user).user_avatar.url
        except:
            pass
        context['id'] = self.object.id
        return context

class AnsDeleteView(DeleteView):
    model = Answer
    fields = ['answer_text']
    template_name = 'asking/question.html'

    def get_success_url(self, **kwargs):
        ask = self.object.ask
        return reverse_lazy('question', kwargs={'pk': ask.id})

def signup(request):
    alert = False
    success = "Вы успешно зарегистрированы!"
    title = "Регистрация"
    button_name = "Зарегистрироваться"
    if request.method == "POST":
        form = SignupForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                user = User.objects.create_user(username=request.POST.get('username'), email=request.POST.get('email'),
                                                password=request.POST.get('password'))
                user.save()
                user_pk = User.objects.get(id=user.pk)
                avatar = request.FILES.get('user_avatar')
                if avatar is not None:
                    user_avatar = Account(user=user_pk, user_avatar=avatar)
                else:
                    user_avatar = Account(user=user_pk, user_avatar="static/asking/img/noavatar.jpg")
                user_avatar.save()
            except IntegrityError:
                alert = False
                return render(request, 'asking/signup.html', {'form': form, 'alert': alert, 'title': title, 'button_name': button_name})
        alert = True
        return render(request, 'asking/signup.html',
                      {'form': form, 'alert': alert, 'success': success, 'title': title, 'button_name': button_name})
    form = SignupForm()
    return render(request, 'asking/signup.html', {'form': form, 'alert': alert, 'success': success, 'title': title, 'button_name': button_name})

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
                  {'index': index, 'title': title, 'tag': tag, 'avatar': avatar(request), 'hot_tags': hot_tags, 'active_users': active_users, 'page_obj': page_obj})


def index_hot(request):
    return index(request, 1)


def login_in(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = auth.authenticate(username=request.POST.get('username'), password=request.POST.get('password'))
            auth.login(request, user)
            return HttpResponseRedirect('/?continue=index')
        return render(request, 'asking/login.html', {'form': form})
    return render(request, 'asking/login.html', {'form': form})


def settings(request):
    title = "Настройки пользователя"
    button_name = "Сохранить изменения"
    success = "Изменения сохранены!"
    if request.user.is_authenticated:
        alert = False
        if request.method == 'POST':
            form = SignupForm(request.POST, request.FILES)
            if form.is_valid():
                request.user.username = request.POST.get('username')
                request.user.email = request.POST.get('email')
                if len(request.POST.get('password')) == 0:
                    request.user.password = User.objects.get(id=request.user.id).password
                else:
                    request.user.password = request.POST.get('password')
                if not request.FILES.get('user_avatar'):
                    request.user.account.user_avatar = Account.objects.get(user=request.user).user_avatar
                else:
                    request.user.account.user_avatar = request.FILES.get('user_avatar')
                request.user.save()
                request.user.account.save()
                user = auth.authenticate(username=request.user.username, password=request.user.password)
                auth.login(request, user)
                alert = True
                return render(request, 'asking/signup.html', {'form': form, 'avatar': avatar(request), 'alert': alert, 'success': success,'title': title, 'button_name': button_name})
            alert = True
            return render(request, 'asking/signup.html', {'form': form, 'avatar': avatar(request), 'alert': alert, 'success': success,'title': title, 'button_name': button_name})
        form = SignupForm(instance=User.objects.get(id=request.user.id))
        return render(request, 'asking/signup.html', {'alert': alert, 'success': success, 'form': form, 'avatar': avatar(request), 'title': title, 'button_name': button_name})
    return HttpResponseRedirect('/?continue=notlogin')

def asklikes(request, current_ask, like_dis):
    try:
        asklike = AskLike.objects.get(user=request.user, ask=current_ask)
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
        current_ask.ask_likes = AskLike.objects.filter(ask=current_ask, like=True).count()
        current_ask.ask_dislikes = AskLike.objects.filter(ask=current_ask, dislike=True).count()
        current_ask.ask_rating = current_ask.ask_likes - current_ask.ask_dislikes
        current_ask.save()
        return False
    except ObjectDoesNotExist:
        if like_dis == 'asklike':
            like = True
            dislike = False
        else:
            dislike = True
            like = False
        asklike = AskLike(user=request.user, ask=current_ask, like=like, dislike=dislike)
        asklike.save()
        current_ask.ask_likes = AskLike.objects.filter(ask=current_ask, like=True).count()
        current_ask.ask_dislikes = AskLike.objects.filter(ask=current_ask, dislike=True).count()
        current_ask.ask_rating = current_ask.ask_likes - current_ask.ask_dislikes
        current_ask.save()
        return True


def answerlikes(request, current_answer, like_dis):
    try:
        anslike = AnswerLike.objects.get(user=request.user, answer=current_answer)
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
        current_answer.answer_likes = AnswerLike.objects.filter(answer=current_answer, like=True).count()
        current_answer.answer_dislikes = AnswerLike.objects.filter(answer=current_answer, dislike=True).count()
        current_answer.save()
        return False
    except ObjectDoesNotExist:
        if like_dis == 'anslike':
            like = True
            dislike = False
        else:
            dislike = True
            like = False
        anslike = AnswerLike(user=request.user, answer=current_answer, like=like, dislike=dislike)
        anslike.save()
        current_answer.answer_likes = AnswerLike.objects.filter(answer=current_answer, like=True).count()
        current_answer.answer_dislikes = AnswerLike.objects.filter(answer=current_answer, dislike=True).count()
        current_answer.save()
        return True

@csrf_exempt
def add_asklike(request):
    if request.method == 'POST':
        ask = request.POST['answer_id']
        current_ask = Ask.objects.get(id=ask)
        like_dis = request.POST['answer']
        try:
            AskLike.objects.get(user=request.user, ask=current_ask, like=False, dislike=False).delete()
        except:
            pass
        if asklikes(request, current_ask, like_dis):
            return JsonResponse({'asklikes': current_ask.ask_likes, 'askdislikes': current_ask.ask_dislikes})
        return JsonResponse({'asklikes': current_ask.ask_likes, 'askdislikes': current_ask.ask_dislikes})

@csrf_exempt
def add_anslike(request):
    if request.method == 'POST':
        answer = request.POST['answer_id']
        current_answer = Answer.objects.get(id=answer)
        like_dis = request.POST['answer']
        try:
            AnswerLike.objects.get(user=request.user, answer=current_answer, like=False, dislike=False).delete()
        except:
            pass
        if answerlikes(request, current_answer, like_dis):
            return JsonResponse({'anslikes': current_answer.answer_likes, 'ansdislikes': current_answer.answer_dislikes})
        return JsonResponse({'anslikes': current_answer.answer_likes, 'ansdislikes': current_answer.answer_dislikes})

@csrf_exempt
def show_asklikes(request):
    if request.method == 'POST':
        ask = request.POST['ask_id']
        current_ask = Ask.objects.get(id=ask)
        try:
            a = AskLike.objects.get(ask=current_ask, user=request.user)
            like = a.like
            dislike = a.dislike
        except:
            like = False
            dislike = False
    return JsonResponse({'like': like, 'dislike': dislike})

@csrf_exempt
def show_anslikes(request):
    if request.method == 'POST':
        ans = request.POST['answer_id']
        current_answer = Answer.objects.get(id=ans)
        try:
            a = AnswerLike.objects.get(answer=current_answer, user=request.user)
            like = a.like
            dislike = a.dislike
        except:
            like = False
            dislike = False
    return JsonResponse({'like': like, 'dislike': dislike})

@csrf_exempt
def rightans(request):
    if request.method == 'POST':
        ans = request.POST['answer_id']
        answer = request.POST['answer']
        current_answer = Answer.objects.get(id=ans)
        if answer == 'right':
            current_answer.answer_is_right = True
        else:
            current_answer.answer_is_right = False
        current_answer.save()
        return JsonResponse({'status': "ok"})


def logout(request):
    if request.user.is_authenticated:
        auth.logout(request)
    return HttpResponseRedirect('/?continue=logout')