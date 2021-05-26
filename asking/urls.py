from django.urls import path
from mysite.settings import MEDIA_URL, MEDIA_ROOT
from .views import index, ask, login_in, logout, QuestDetailView, settings, signup, index_hot
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls import handler404

urlpatterns = [
	path('', index, name='index'),
	path('hot/', index_hot, name='index_hot'),
	path('login/', login_in, name='login'),
	path('signup/', signup, name='signup'),
	path('settings/', settings, name='settings'),
	path('ask/', ask, name='ask'),
	path('<int:pk>/', QuestDetailView.as_view(), name='question'),
	path('logout/', logout, name='logout'),
	path('tag/<slug:tag_slug>/', index, name='index_tag'),
]
urlpatterns += static(MEDIA_URL, document_root=MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()