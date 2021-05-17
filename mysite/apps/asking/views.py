from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import Ask, Answer

def index(request):
	latest_asks_list = Ask.objects.order_by('-pub_date')[:5]
	return render(request, 'asks/list.html', {'latest_asks_list': latest_asks_list})
	
def detail(request, ask_id):
	try:
		a = Ask.objects.get( id = ask_id )
	except:
		raise Http404("Вопрос не найден!")
	last_answers_list = a.answer_set.order_by('-id')[:10]
		
	return render(request, 'asks/detail.html', {'ask': a})
	
def get_answer(request, ask_id):
	try:
		a = Ask.objects.get( id = ask_id )
	except:
		raise Http404("Вопрос не найден!")
		
	return render(request, 'asks/detail.html', {'ask': a})
	
	a.answer_set.create(author_name = request.POST['name'], answer_text = request.POST['text'])
	
	return HttpResponseRedirect(reverse('asks:detail', args = a.id,))
# Create your views here.
