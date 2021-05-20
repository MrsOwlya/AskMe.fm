import datetime
from django.db import models

from django.utils import timezone

# Create your models here.

class User(models.Model):
	user_login = models.CharField('Имя пользователя', max_length = 20)
	user_email = models.CharField('Емейл', max_length = 50)
	user_password = models.CharField('Пароль', max_length = 50)
	user_avatar = models.ImageField('Аватарка')
	user_rating = models.IntegerField('Рейтинг')

	def __str__(self):
		return self.user_login

class Ask(models.Model):
	ask_title = models.CharField('Вопрос', max_length = 200)
	asker_name = models.ForeignKey(User, on_delete = models.CASCADE)
	ask_explane = models.TextField('Пояснение вопроса')
	ask_date = models.DateTimeField('Дата публикации')
	ask_tags = models.CharField('Тег', max_length = 50)
	ask_answers = models.IntegerField('Кол-во ответов')
	ask_rating = models.IntegerField('Рейтинг вопроса')

	def __str__(self):
		return self.ask_title
		
	def was_asked_earlier(self):
		return self.ask_date >= (timezone.now() - datetime.timedelta(days = 7))
		
	class Meta:
		verbose_name = 'Вопрос'
		verbose_name_plural = 'Вопросы'
	
class Answer(models.Model):
	ask = models.ForeignKey(Ask, on_delete = models.CASCADE)
	answerer_name = models.ForeignKey(User, on_delete = models.CASCADE)
	answer_text = models.TextField('Текст ответа')
	answer_date = models.DateTimeField('Дата ответа')
	answer_likes = models.IntegerField('Кол-во лайков')
	
	def __str__(self):
		return self.answerer_name
		
	class Meta:
		verbose_name = 'Ответ'
		verbose_name_plural = 'Ответы'

class Tag(models.Model):
	ask_id = models.ForeignKey(Ask, on_delete = models.CASCADE)
	tag_name = models.CharField('Tag', max_length = 50)
	tag_rating = models.IntegerField('Популярность тега')

	def __str__(self):
		return self.tag_name

class Like(models.Model):
	answer = models.ForeignKey(Answer, on_delete = models.CASCADE)
	user = models.ForeignKey(User, on_delete = models.CASCADE)
	likes_count = models.IntegerField('Кол-во лайков')

	def __str__(self):
		return self.likes_count