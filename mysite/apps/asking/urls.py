from django.urls import path

from . import views

app_name = 'asking'
urlpatterns = [
	path('', views.index, name = 'index'),
	path('login/', views.login, name = 'login'),
	path('signup/', views.signup, name = 'signup'),
	path('ask/', views.ask, name='ask'),
	path('<int:ask_id>/', views.question, name = 'question'),
]
