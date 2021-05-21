from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render

from .models import Ask, Answer, User, Like, Tag

def base(request):
	return render(request, 'base.html')

def login(request):
	return render(request, 'asking/login.html')

def signup(request):
	return render(request, 'asking/signup.html')

def ask(request):
	return render(request, 'asking/ask.html')

def index(request):
	index = Ask.objects.order_by('-ask_date')[:5]
	return render(request, 'asking/index.html', {'index': index})
	
def question(request):

	return render(request, 'asking/question.html')
# Create your views here.
