from django.conf.urls import url, include

from ptpgo import views

urlpatterns = [
	url(r'^rest/?$', views.rest_home, name='rest_home'),

	url(r'^rest/authenticate/?$', views.authenticate, name='authenticate'),
	url(r'^rest/check_auth/?$', views.check_auth, name='check_auth'),
	
	url(r'^$', views.home, name='home'),
]
