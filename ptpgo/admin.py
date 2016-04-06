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

# from ptpgo.models import CarType, CarMark, CarModel, CarGeneration, CarSerie, CarModification, CarCharacteristic, CarCharacteristicValue

# База авто
# admin.site.register(CarType)
# admin.site.register(CarMark)
# admin.site.register(CarModel)
# admin.site.register(CarGeneration)
# admin.site.register(CarSerie)
# admin.site.register(CarModification)
# admin.site.register(CarCharacteristic)
# admin.site.register(CarCharacteristicValue)
