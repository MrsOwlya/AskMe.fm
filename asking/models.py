import datetime
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from taggit.managers import TaggableManager

# Create your models here.


class Account(models.Model):
    user = models.OneToOneField(User, related_name='account', null=False, verbose_name='Пользователь', on_delete=models.CASCADE)
    user_avatar = models.ImageField(null=True, blank=True, verbose_name='Аватарка', upload_to='static/asking/img/')
    user_rating = models.IntegerField(blank=True, default=0, verbose_name='Рейтинг')

    def __str__(self):
        return str(self.user)

    def get_absolute_url(self):
        return f'/settings/{self.id}/'

class Ask(models.Model):
    ask_title = models.CharField(verbose_name='Вопрос', max_length=200)
    asker_name = models.ForeignKey(User, on_delete=models.CASCADE)
    ask_explane = models.TextField(verbose_name='Пояснение вопроса')
    ask_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')
    ask_tags = TaggableManager()
    ask_likes = models.IntegerField(default=0, verbose_name='Кол-во лайков')
    ask_dislikes = models.IntegerField(default=0, verbose_name='Кол-во дизлайков')
    ask_rating = models.IntegerField(default=0, verbose_name='Рейтинг вопроса')

    def __str__(self):
        return self.ask_title

    def get_absolute_url(self):
        return f'/{self.id}/'

    def was_asked_earlier(self):
        return self.ask_date >= (timezone.now() - datetime.timedelta(days=7))

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'


class Answer(models.Model):
    ask = models.ForeignKey(Ask, on_delete=models.CASCADE, related_name='ask_answer', null=True, blank=True)
    answerer_name = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    answer_text = models.TextField(verbose_name='Текст ответа')
    answer_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата ответа')
    answer_likes = models.IntegerField(default=0, verbose_name='Кол-во лайков')
    answer_dislikes = models.IntegerField(default=0, verbose_name='Кол-во дизлайков')
    answer_is_right = models.BooleanField(default=False, verbose_name="Правильный ответ")

    def __str__(self):
        return self.answer_text

    def get_absolute_url(self):
        return f'/{self.ask.id}/'

    class Meta:
        verbose_name = 'Ответ'
        verbose_name_plural = 'Ответы'


class AnswerLike(models.Model):
    answer = models.ForeignKey(Answer, related_name='answer_like', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    like = models.BooleanField(default=False, verbose_name='Лайк')
    dislike = models.BooleanField(default=False, verbose_name='Дизлайк')

    def __str__(self):
        return str(self.answer)

class AskLike(models.Model):
    ask = models.ForeignKey(Ask, related_name='ask_like', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    like = models.BooleanField(default=False, verbose_name='Лайк')
    dislike = models.BooleanField(default=False, verbose_name='Дизлайк')

    def __str__(self):
        return str(self.ask)