# -*- coding: utf-8 -*-
from django.utils import timezone
from django.db import models



class Clients(models.Model):

	class Meta:
		verbose_name_plural = 'Клиенты: Аккаунт'

	def __str__(self):
		return self.email + '; id: ' + str(self.id)


	email                     = models.CharField(max_length=100)
	password                  = models.CharField(max_length=1000)

	fio                       = models.CharField(max_length=255, blank=True, null=True)
	about                     = models.TextField(blank=True, null=True)

	phone                     = models.CharField(max_length=255, blank=True, null=True)
	additional_contacts       = models.CharField(max_length=1000, blank=True, null=True)

	confirm_code              = models.CharField(max_length=255, blank=True, null=True, default="")

	response_time             = models.CharField(max_length=255, blank=True, null=True)

	registered                = models.DateTimeField('registered', default=timezone.now)
	updated                   = models.DateTimeField('updated', default=timezone.now)



class Tokens(models.Model):

	class Meta:
		verbose_name_plural = "Клиенты: Токены авторизации"

	def __str__(self):
		return self.client.email + ': ' + self.token

	client                    = models.ForeignKey('ptpgo.Clients')
	token                     = models.CharField(max_length=255)
	device_info               = models.CharField(max_length=1000, default="", blank=True, null=True)
	last_login                = models.DateTimeField('last login', default=timezone.now)
	last_activity             = models.DateTimeField('last activity', default=timezone.now)



class ClientPhotos(models.Model):

	class Meta:
		verbose_name_plural = "Клиенты: Фотографии"

	def __str__(self):
		return 'id: ' + str(self.id) + '; client: ' + str(self.client.email)

	client                    = models.ForeignKey('ptpgo.Clients')
	photo                     = models.FileField(upload_to='client_photos/', blank=False, null=False)
	timestamp                 = models.DateTimeField('added/updated', default=timezone.now)



class ClientRatings(models.Model):

	class Meta:
		verbose_name_plural = "Клиенты: Рейтинг"

	def __str__(self):
		return self.client.email + ': ' + str(self.rating)

	client                    = models.ForeignKey('ptpgo.Clients')
	rating                    = models.FloatField(default=0.0)
	rated_by                  = models.IntegerField(default=0)
	timestamp                 = models.DateTimeField('added', default=timezone.now)



class ClientSiteNotifications(models.Model):

	class Meta:
		verbose_name_plural = "Клиенты: Уведомления на сайте"

	def __str__(self):
		return self.notification_type + ' | client: ' + self.client.email

	client                    = models.ForeignKey('ptpgo.Clients')
	notification_type         = models.CharField(max_length=255)
	notification_data         = models.CharField(max_length=255)
	checked                   = models.BooleanField(default=False)
	timestamp                 = models.DateTimeField('added', default=timezone.now)



class ClientNotificationsLog(models.Model):

	class Meta:
		verbose_name_plural = "Клиенты: Лог sms и email уведомлений"

	def __str__(self):
		return self.destination_system + ' | client: ' + self.client.email

	client                    = models.ForeignKey('ptpgo.Clients')
	notification_type         = models.CharField(max_length=255)
	notification_data         = models.CharField(max_length=255)
	destination_system        = models.CharField(max_length=255)
	destination_details       = models.CharField(max_length=255)
	timestamp                 = models.DateTimeField('added', default=timezone.now)

#######################################################################
#######################################################################
#######################################################################



class ListBoat(models.Model):

	class Meta:
		verbose_name_plural = 'Объявления: Водный транспорт'

	def __str__(self):
		return 'ID: ' + str(self.id) + ' | by ' + self.client.email

	client                    = models.ForeignKey('ptpgo.Clients')

	boat_type                 = models.CharField(max_length=255, blank=True, null=True)
	boat_builder              = models.CharField(max_length=255, blank=True, null=True)
	boat_model                = models.CharField(max_length=255, blank=True, null=True)
	boat_length               = models.CharField(max_length=255, blank=True, null=True)
	boat_build_year           = models.CharField(max_length=32)

	location                  = models.CharField(max_length=1000, blank=True, null=True)

	description               = models.CharField(max_length=10000, blank=True, null=True)
	amenities                 = models.CharField(max_length=10000, blank=True, null=True) # удобства

	guest_capacity            = models.IntegerField(default=0)
	cabins                    = models.IntegerField(default=0)
	single_beds               = models.IntegerField(default=0)
	double_beds               = models.IntegerField(default=0)

	avail_date_ranges         = models.CharField(max_length=1000, blank=True, null=True)
	not_avail_date_ranges     = models.CharField(max_length=1000, blank=True, null=True)

	with_captain              = models.BooleanField(default=True)
	fuel_included             = models.BooleanField(default=True)

	day_price                 = models.CharField(max_length=255, blank=True, null=True)
	week_price                = models.CharField(max_length=255, blank=True, null=True)
	month_price               = models.CharField(max_length=255, blank=True, null=True)

	canceled                  = models.BooleanField(default=False)

	timestamp_edited          = models.DateTimeField('date updated', default=timezone.now)
	timestamp_added           = models.DateTimeField('date listed', default=timezone.now)



class ListBoatPhotos(models.Model):

	class Meta:
		verbose_name_plural = 'Объявления: Водный транспорт - фотографии'

	def __str__(self):
		return 'Объявление id: ' + str(self.boat.id)

	boat                      = models.ForeignKey('ptpgo.ListBoat')
	photo                     = models.FileField(upload_to='boat_photos/', blank=False, null=False)
	timestamp                 = models.DateTimeField('added', default=timezone.now)




# class Orders(models.Model):
# 	pass

# class Reviews(models.Model):
# 	pass

#######################################################################
#######################################################################
#######################################################################



# Вид транспорта
class CarType(models.Model):

	class Meta:
		verbose_name_plural = 'База авто: Вид транспорта'

	def __str__(self):
		return self.name

	name                      = models.CharField(max_length=255) # пример: легковые



# Марка автомобиля
class CarMark(models.Model):

	class Meta:
		verbose_name_plural = 'База авто: Марка автомобиля'

	def __str__(self):
		return self.name

	id_car_mark               = models.IntegerField(default=0)
	name                      = models.CharField(max_length=255) # Название марки
	name_rus                  = models.CharField(max_length=255, blank=True, null=True) # Название марки на русском

	id_car_type               = models.ForeignKey('ptpgo.CarType') # Связь: Вид транспорта



# Модель автомобиля
class CarModel(models.Model):

	class Meta:
		verbose_name_plural = 'База авто: Модель автомобиля'

	def __str__(self):
		return self.name

	id_car_model              = models.IntegerField(default=0)
	name                      = models.CharField(max_length=255) # Название модели
	name_rus                  = models.CharField(max_length=255, blank=True, null=True) # Название модели на русском

	id_car_mark               = models.IntegerField(default=0) # Связь: Марка автомобиля



# Поколение моделей
class CarGeneration(models.Model):

	class Meta:
		verbose_name_plural = 'База авто: Поколение моделей'

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
		verbose_name_plural = 'База авто: Серия автомобиля'

	def __str__(self):
		return self.name

	id_car_serie              = models.IntegerField(default=0)
	name                      = models.CharField(max_length=255) # Название

	id_car_model              = models.IntegerField(default=0) # Связь: Модель автомобиля
	id_car_generation         = models.IntegerField(blank=True, null=True) # Связь: Поколение моделей



# Модификация автомобиля
class CarModification(models.Model):

	class Meta:
		verbose_name_plural = 'База авто: Модификация автомобиля'

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
		verbose_name_plural = 'База авто: Значение характеристик автомобиля'

	def __str__(self):
		return 'ID названия характеристики: ' + str(self.id_car_characteristic) + ' | Модификация id: ' + str(self.id_car_modification)

	id_car_characteristic_value = models.IntegerField(default=0)
	value                     = models.CharField(max_length=255) # Значение
	unit                      = models.CharField(max_length=255, blank=True, null=True) # Единица измерения

	id_car_characteristic     = models.IntegerField(default=0) # Связь: Название характеристики
	id_car_modification       = models.IntegerField(default=0) # Связь: Модификация автомобиля



# Название характеристики автомобиля
class CarCharacteristic(models.Model):

	class Meta:
		verbose_name_plural = 'База авто: Название характеристики'

	def __str__(self):
		return self.name

	id_car_characteristic     = models.IntegerField(default=0)
	name                      = models.CharField(max_length=255, blank=True, null=True) # Название
	parent                    = models.IntegerField(blank=True, null=True)

