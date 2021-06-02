from django.urls import path

from asking import views
from mysite.settings import MEDIA_URL, MEDIA_ROOT
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
	path('hot_tags/', views.hot_tags, name='hot_tags'),
	path('active_users/', views.active_users, name='active_users'),
	path('<int:pk>/', views.QuestDetailView.as_view(), name='question'),
	path('<int:pk>/update', views.QuestUpdateView.as_view(), name='askupdate'),
	path('<int:pk>/delete', views.QuestDeleteView.as_view(), name='askdelete'),
	path('<int:pk>/answer_update', views.AnsUpdateView.as_view(), name='ansupdate'),
	path('<int:pk>/answer_delete', views.AnsDeleteView.as_view(), name='ansdelete'),
	path('signup/', views.signup, name='signup'),
	path('ask/', views.ask, name='ask'),
	path('', views.index, name='index'),
	path('hot/', views.index_hot, name='index_hot'),
	path('login/', views.login_in, name='login'),
	path('settings/', views.settings, name='settings'),
	path('tag/<slug:tag_slug>/', views.index, name='index_tag'),
	path('add_asklike/', views.add_asklike, name='add_asklike'),
	path('add_anslike/', views.add_anslike, name='add_anslike'),
	path('show_asklikes/', views.show_asklikes, name='show_asklikes'),
	path('show_anslikes/', views.show_anslikes, name='show_anslikes'),
	path('rightans/', views.rightans, name='rightans'),
	path('logout/', views.logout, name='logout'),
]
urlpatterns += static(MEDIA_URL, document_root=MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()