import datetime
from django.db import models

from django.utils import timezone

# Create your models here.

class Ask(models.Model):
	ask_title = models.CharField('Вопрос', max_length = 200)
	ask_explane = models.TextField('Пояснение вопроса')
	pub_date = models.DateTimeField('Дата публикации')
	
	def __str__(self):
		return self.ask_title
		
	def was_asked_earlier(self):
		return self.pub_date >= (timezone.now() - datetime.timedelta(days = 7))
		
	class Meta:
		verbose_name = 'Вопрос'
		verbose_name_plural = 'Вопросы'
	
class Answer(models.Model):
	ask = models.ForeignKey(Ask, on_delete = models.CASCADE)
	author_name = models.CharField('Имя автора', max_length = 50)
	answer_text = models.TextField('Текст ответа')
	
	def __str__(self):
		return self.author_name
		
	class Meta:
		verbose_name = 'Ответ'
		verbose_name_plural = 'Ответы'
