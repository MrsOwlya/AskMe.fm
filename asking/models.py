import datetime
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from taggit.managers import TaggableManager

# Create your models here.

class Account(models.Model):
    user = models.OneToOneField(User, related_name='account', null=False, verbose_name='Пользователь', on_delete=models.DO_NOTHING)
    user_avatar = models.ImageField(null=True, blank=True, verbose_name=u'Аватарка', upload_to="static/asking/img")
    user_rating = models.IntegerField(blank=True, default=0, verbose_name=u'Рейтинг')

    def __str__(self):
        return self.user.username


class Ask(models.Model):
    ask_title = models.CharField(verbose_name=u'Вопрос', max_length=200)
    asker_name = models.ForeignKey(User, on_delete=models.CASCADE)
    ask_explane = models.TextField(verbose_name=u'Пояснение вопроса')
    ask_date = models.DateTimeField(auto_now_add=True, verbose_name=u'Дата публикации')
    ask_tags = TaggableManager()
    ask_rating = models.IntegerField(default=0, verbose_name=u'Рейтинг вопроса')

    def __str__(self):
        return self.ask_title

    def was_asked_earlier(self):
        return self.ask_date >= (timezone.now() - datetime.timedelta(days=7))

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'


class Answer(models.Model):
    ask = models.ForeignKey(Ask, on_delete=models.CASCADE, related_name='ask_answer', null=True, blank=True)
    answerer_name = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    answer_text = models.TextField(verbose_name=u'Текст ответа')
    answer_date = models.DateTimeField(auto_now_add=True, verbose_name=u'Дата ответа')
    answer_likes = models.IntegerField(default=0, verbose_name=u'Кол-во лайков')
    answer_is_right = models.BooleanField(default=False, verbose_name="Правильный ответ")

    def __str__(self):
        return self.answer_text

    class Meta:
        verbose_name = 'Ответ'
        verbose_name_plural = 'Ответы'


class AnswerLike(models.Model):
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    like = models.BooleanField(default=False, verbose_name=u'Кол-во лайков')
    dislike = models.BooleanField(default=False, verbose_name=u'Кол-во дизлайков')

    def __str__(self):
        return self.answer

class AskLike(models.Model):
    ask = models.ForeignKey(Ask, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    like = models.BooleanField(default=False, verbose_name=u'Кол-во лайков')
    dislike = models.BooleanField(default=False, verbose_name=u'Кол-во дизлайков')

    def __str__(self):
        return self.ask