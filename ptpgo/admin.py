from django.contrib import admin

from ptpgo.models import Clients
from ptpgo.models import Tokens
from ptpgo.models import ClientPhotos
from ptpgo.models import ClientRatings


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