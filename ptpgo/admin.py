from django.contrib import admin

from ptpgo.models import Clients
from ptpgo.models import ClientPhotos
from ptpgo.models import ClientRatings
from ptpgo.models import ClientSiteNotifications
from ptpgo.models import ClientNotificationsLog

admin.site.register(Clients)
admin.site.register(ClientPhotos)
admin.site.register(ClientRatings)
admin.site.register(ClientSiteNotifications)
admin.site.register(ClientNotificationsLog)
