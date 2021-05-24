from django.urls import path
from mysite.settings import MEDIA_URL, MEDIA_ROOT
from .views import index, ask, login_in, logout, QuestDetailView, settings, SignupView
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls import handler404

urlpatterns = [
	path('', index, name='index'),
	path('login/', login_in, name='login'),
	path('signup/', SignupView.as_view(), name='signup'),
	path('settings/', settings, name='settings'),
	path('ask/', ask, name='ask'),
	path('<int:pk>/', QuestDetailView.as_view(), name='question'),
	path('logout/', logout, name='logout')
]
urlpatterns += static(MEDIA_URL, document_root=MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()