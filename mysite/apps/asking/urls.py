from django.urls import path

from . import views

app_name = 'asking'
urlpatterns = [
	path('', views.index, name = 'asking/index'),
	path('login/', views.login, name = 'asking/login'),
	path('signup/', views.signup, name = 'asking/signup'),
	path('<int:ask_id>/', views.question, name = 'asking/question'),
	path('<int:ask_id>/get_answer/', views.get_answer, name = 'asking`/get_answer'),
]
