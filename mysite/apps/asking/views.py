from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render

from .models import Ask, Answer

def base(request):
	return render(request, 'base.html')

def login(request):
	return render(request, 'asking/login.html')

def signup(request):
	return render(request, 'asking/signup.html')

def index(request):
	latest_asks_list = Ask.objects.order_by('-ask_date')[:5]
	return render(request, 'asking/index.html', {'latest_asks_list': latest_asks_list})
	
def question(request, ask_id):
	try:
		a = Ask.objects.get( id = ask_id )
	except:
		raise ObjectDoesNotExist("Вопрос не найден!")
	last_answers_list = a.answer_set.order_by('-id')[:10]
		
	return render(request, 'asking/question.html', {'ask': a})
# Create your views here.
