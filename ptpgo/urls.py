from django.conf.urls import url, include
from django.contrib import admin

from ptpgo import views

urlpatterns = [

	url(r'^admin/', admin.site.urls),

]
