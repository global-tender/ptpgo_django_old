from django.conf.urls import url, include

from rest_framework import routers
from gl_rent import views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)

urlpatterns = [
	url(r'^rest/', include(router.urls)),
]
