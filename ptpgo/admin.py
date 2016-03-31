from django.contrib import admin

from ptpgo.models import CarType, CarMark, CarModel, CarGeneration, CarSerie, CarModification, CarCharacteristic, CarCharacteristicValue

# База авто
admin.site.register(CarType)
admin.site.register(CarMark)
admin.site.register(CarModel)
admin.site.register(CarGeneration)
admin.site.register(CarSerie)
admin.site.register(CarModification)
admin.site.register(CarCharacteristic)
admin.site.register(CarCharacteristicValue)
