from django.conf.urls import url, include

from ptpgo import views

urlpatterns = [
	url(r'^rest/?$', views.rest_home, name='rest_home'),
	
	url(r'^$', views.home, name='home'),
]
