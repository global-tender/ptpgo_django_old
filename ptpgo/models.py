# -*- coding: utf-8 -*-
from django.utils import timezone
from django.db import models

class Clients(models.Model):

	class Meta:
		verbose_name_plural = 'Clients'

	def __str__(self):
		return self.email + '; id: ' + str(self.id)


	email                     = models.CharField(max_length=100)
	password                  = models.CharField(max_length=1000)

	fio                       = models.CharField(max_length=1000, blank=True, null=True)
	about                     = models.TextField(blank=True, null=True)

	phone                     = models.CharField(max_length=1000, blank=True, null=True)
	additional_contacts       = models.CharField(max_length=1000, blank=True, null=True)

	confirm_code              = models.CharField(max_length=1000, blank=True, null=True, default="")

	registered                = models.DateTimeField('registered', default=timezone.now)
	updated                   = models.DateTimeField('updated', default=timezone.now)

class Tokens(models.Model):

	class Meta:
		verbose_name_plural = "Tokens"

	def __str__(self):
		return self.client.email + ': ' + self.token

	client                    = models.ForeignKey('ptpgo.Clients')
	token                     = models.CharField(max_length=1000)
	device_info               = models.CharField(max_length=1000, default="", blank=True, null=True)
	last_login                = models.DateTimeField('last login', default=timezone.now)
	last_activity             = models.DateTimeField('last activity', default=timezone.now)

class ClientPhotos(models.Model):

	class Meta:
		verbose_name_plural = "ClientPhotos"

	def __str__(self):
		return 'id: ' + str(self.id) + '; client: ' + str(self.client.email)

	client                    = models.ForeignKey('ptpgo.Clients')
	photo                     = models.FileField(upload_to='client_photos/', blank=False, null=False)
	updated                   = models.DateTimeField('updated', default=timezone.now)

class ClientRatings(models.Model):

	class Meta:
		verbose_name_plural = "ClientRatings"

	def __str__(self):
		return self.client.email + ': ' + str(self.rating)

	client                    = models.ForeignKey('ptpgo.Clients')
	rating                    = models.FloatField(default=0.0)
	updated                   = models.DateTimeField('updated', default=timezone.now)




#######################################################################
#######################################################################
#######################################################################


# Вид транспорта
class CarType(models.Model):

	class Meta:
		verbose_name_plural = 'Вид транспорта'

	def __str__(self):
		return self.name

	name                      = models.CharField(max_length=255) # пример: легковые



# Марка автомобиля
class CarMark(models.Model):

	class Meta:
		verbose_name_plural = 'Марка автомобиля'

	def __str__(self):
		return self.name

	id_car_mark               = models.IntegerField(default=0)
	name                      = models.CharField(max_length=255) # Название марки
	name_rus                  = models.CharField(max_length=255, blank=True, null=True) # Название марки на русском

	id_car_type               = models.ForeignKey('ptpgo.CarType') # Связь: Вид транспорта



# Модель автомобиля
class CarModel(models.Model):

	class Meta:
		verbose_name_plural = 'Модель автомобиля'

	def __str__(self):
		return self.name

	id_car_model              = models.IntegerField(default=0)
	name                      = models.CharField(max_length=255) # Название модели
	name_rus                  = models.CharField(max_length=255, blank=True, null=True) # Название модели на русском

	id_car_mark               = models.IntegerField(default=0) # Связь: Марка автомобиля



# Поколение моделей
class CarGeneration(models.Model):

	class Meta:
		verbose_name_plural = 'Поколение моделей'

	def __str__(self):
		return self.name

	id_car_generation         = models.IntegerField(default=0)
	name                      = models.CharField(max_length=255) # Название
	year_begin                = models.CharField(max_length=255, default="", blank=True, null=True) # Год начала выпуска
	year_end                  = models.CharField(max_length=255, default="", blank=True, null=True) # Год окончания выпуска

	id_car_model              = models.IntegerField(default=0) # Связь: Модель автомобиля



# Серия автомобиля
class CarSerie(models.Model):

	class Meta:
		verbose_name_plural = 'Серия автомобиля'

	def __str__(self):
		return self.name

	id_car_serie              = models.IntegerField(default=0)
	name                      = models.CharField(max_length=255) # Название

	id_car_model              = models.IntegerField(default=0) # Связь: Модель автомобиля
	id_car_generation         = models.IntegerField(blank=True, null=True) # Связь: Поколение моделей



# Модификация автомобиля
class CarModification(models.Model):

	class Meta:
		verbose_name_plural = 'Модификация автомобиля'

	def __str__(self):
		return self.name

	id_car_modification       = models.IntegerField(default=0)
	name                      = models.CharField(max_length=255) # Название

	start_production_year     = models.IntegerField(blank=True, null=True)
	end_production_year       = models.IntegerField(blank=True, null=True)
	price_min                 = models.IntegerField(blank=True, null=True)
	price_max                 = models.IntegerField(blank=True, null=True)

	id_car_model              = models.IntegerField(default=0) # Связь: Модель автомобиля
	id_car_serie              = models.IntegerField(default=0) # Связь: Серия автомобиля



# Значение характеристик автомобиля
class CarCharacteristicValue(models.Model):

	class Meta:
		verbose_name_plural = 'Значение характеристик автомобиля'

	def __str__(self):
		return self.car_characteristic.name + ' | Модификация id: ' + str(self.car_modification.id)

	id_car_characteristic_value = models.IntegerField(default=0)
	value                     = models.CharField(max_length=255) # Значение
	unit                      = models.CharField(max_length=255, blank=True, null=True) # Единица измерения

	id_car_characteristic     = models.IntegerField(default=0) # Связь: Название характеристики
	id_car_modification       = models.IntegerField(default=0) # Связь: Модификация автомобиля



# Название характеристики автомобиля
class CarCharacteristic(models.Model):

	class Meta:
		verbose_name_plural = 'Название характеристики'

	def __str__(self):
		return self.name

	id_car_characteristic     = models.IntegerField(default=0)
	name                      = models.CharField(max_length=255, blank=True, null=True) # Название
	parent                    = models.IntegerField(blank=True, null=True)

