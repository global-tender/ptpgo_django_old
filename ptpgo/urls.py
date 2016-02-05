from django.conf.urls import url, include

from ptpgo import views

urlpatterns = [
	url(r'^rest/?$', views.rest_home, name='rest_home'),

	url(r'^rest/authenticate/?$', views.authenticate, name='authenticate'),
	url(r'^rest/check_auth/?$', views.check_auth, name='check_auth'),
	url(r'^rest/register/?$', views.register, name='register'),
	url(r'^rest/confirm_register/?$', views.confirm_register, name='confirm_register'),
	
	url(r'^$', views.home, name='home'),
]
