from django.urls import path

from . import views

app_name = 'asks'
urlpatterns = [
	path('', views.index, name = 'index'),
	path('<int:ask_id>/', views.detail, name = 'detail'),
	path('<int:ask_id>/get_answer/', views.get_answer, name = 'get_answer'),
]
