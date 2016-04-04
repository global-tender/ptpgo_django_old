from django.conf.urls import url, include
from django.contrib import admin

from ptpgo import views, views_client

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.index, name='index'),

    url(r'^signin/?$', views_client.signin, name='signin'),
    url(r'^signup/?$', views_client.signup, name='signup'),
    url(r'^signout/?$', views_client.signout, name='signout'),

    url(r'^cabinet/?$', views_client.cabinet, name='cabinet'),

    url(r'^robots.txt$', views.robots, name='robots.txt'),
]
