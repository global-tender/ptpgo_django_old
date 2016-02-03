from django.contrib import admin

from ptpgo.models import Clients
from ptpgo.models import Tokens
from ptpgo.models import ClientPhotos
from ptpgo.models import ClientRatings
from ptpgo.models import Country
from ptpgo.models import City

admin.site.register(Clients)
admin.site.register(Tokens)
admin.site.register(ClientPhotos)
admin.site.register(ClientRatings)
admin.site.register(Country)
admin.site.register(City)