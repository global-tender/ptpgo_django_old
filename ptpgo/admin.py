from django.contrib import admin

from ptpgo.models import Clients
from ptpgo.models import Tokens
from ptpgo.models import ClientPhotos
from ptpgo.models import ClientRatings
from ptpgo.models import ClientSiteNotifications
from ptpgo.models import ClientNotificationsLog

from ptpgo.models import ListBoat
from ptpgo.models import ListBoatPhotos

from ptpgo.models import OrderBoat

from ptpgo.models import Reviews

from ptpgo.models import CarType, CarMark, CarModel, CarGeneration, CarSerie, CarModification, CarCharacteristic, CarCharacteristicValue

admin.site.register(Clients)
admin.site.register(Tokens)
admin.site.register(ClientPhotos)
admin.site.register(ClientRatings)


admin.site.register(CarType)
admin.site.register(CarMark)
admin.site.register(CarModel)
admin.site.register(CarGeneration)
admin.site.register(CarSerie)
admin.site.register(CarModification)
admin.site.register(CarCharacteristic)
admin.site.register(CarCharacteristicValue)


admin.site.register(ClientSiteNotifications)
admin.site.register(ClientNotificationsLog)


admin.site.register(ListBoat)
admin.site.register(ListBoatPhotos)

admin.site.register(OrderBoat)
admin.site.register(Reviews)
