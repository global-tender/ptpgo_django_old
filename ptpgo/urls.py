from django.conf.urls import url, include

from ptpgo import views, views_client

urlpatterns = [
	url(r'^rest/?$', views.rest_index, name='rest_index'),

	url(r'^rest/authenticate/?$', views_client.authenticate, name='authenticate'),
	url(r'^rest/check_auth/?$', views_client.check_auth, name='check_auth'),
	url(r'^rest/register_with_email/?$', views_client.register_with_email, name='register_with_email'),
	url(r'^rest/confirm_email/?$', views_client.confirm_email, name='confirm_email'),

	url(r'^socauth/(?P<arg>\w+)/?$', views_client.social_auth, name='social_auth'),

	url(r'^$', views.index, name='index'),
]
