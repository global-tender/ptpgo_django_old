# -*- coding: utf-8 -*-
from django.utils import timezone
from django.db import models



class Clients(models.Model):

	class Meta:
		verbose_name_plural = 'Клиенты: Аккаунт'

	def __str__(self):
		return 'id: ' + str(self.id)

	email                     = models.CharField(max_length=100, blank=True, null=True) # E-Mail
	password                  = models.CharField(max_length=1000, blank=True, null=True) # Пароль

	first_name                = models.CharField(max_length=255, blank=True, null=True) # Имя
	last_name                 = models.CharField(max_length=255, blank=True, null=True) # Фамилия

	# Регистрация/Авторизация через соц. сети
	vk_user_id                = models.CharField(max_length=255, blank=True, null=True) # Связь: VK



	about                     = models.TextField(blank=True, null=True) # О себе

	phone                     = models.CharField(max_length=255, blank=True, null=True) # Номер телефона, только цифры, без пробелов
	additional_contacts       = models.CharField(max_length=1000, blank=True, null=True) # Дополнительные контакты, в свободной форме

	email_confirmed           = models.BooleanField(default=False) # Был ли подтвержден E-Mail
	phone_confirmed           = models.BooleanField(default=False) # Был ли подтвержден номер телефона

	email_confirm_code        = models.CharField(max_length=255, blank=True, null=True) # Код потверждения E-Mail адреса
	phone_confirm_code        = models.CharField(max_length=255, blank=True, null=True) # Код потверждения номер телефона

	# Среднее время отклика на заказ, подсчитывается и изменяется по отклику
	response_time             = models.CharField(max_length=32, blank=True, null=True)
	# В процентах количество откликов на заказ (пример: 100%)
	response_rate             = models.CharField(max_length=32, blank=True, null=True)

	honors                    = models.IntegerField(default=0) # Награды - баллы

	registered                = models.DateTimeField('registered', default=timezone.now) # Дата/время регистрации
	updated                   = models.DateTimeField('updated', default=timezone.now) # Дата/время обновления данных пользователя, самим пользователем



class Tokens(models.Model):

	class Meta:
		verbose_name_plural = "Клиенты: Токены авторизации пользователей"

	def __str__(self):
		return str(self.client.id) + ': ' + self.token

	client                    = models.ForeignKey('ptpgo.Clients') # Связь: Клиент
	token                     = models.CharField(max_length=255) # Токен авторизации
	device_info               = models.CharField(max_length=1000, default="", blank=True, null=True) # Информация об устройстве пользователя
	last_login                = models.DateTimeField('last login', default=timezone.now) # Дата/время авторизации
	last_activity             = models.DateTimeField('last activity', default=timezone.now) # Дата/время активности: новый заказ, объявление или отзыв



class AuthVk(models.Model):

	class Meta:
		verbose_name_plural = 'Клиенты: Авторизация через vk.com'

	def __str__(self):
		return 'user_id: ' + self.vk_user_id

	vk_user_id                = models.CharField(max_length=255) # Связь с аккаунтом
	email                     = models.CharField(max_length=255, blank=True, null=True)

	access_token              = models.CharField(max_length=255, default="") # Токен доступа к данным пользователя
	expires_in                = models.CharField(max_length=255, default="") # Время жизни токена доступа

	profile                   = models.CharField(max_length=10000, blank=True, null=True) # json данных пользователя

	updated                   = models.DateTimeField('updated', default=timezone.now) # Дата/время обновления данных пользователя, при повторной авторизации




#######################################################################
#######################################################################
#######################################################################



class ClientPhotos(models.Model):

	class Meta:
		verbose_name_plural = "Клиенты: Фотографии"

	def __str__(self):
		return 'id: ' + str(self.id) + '; client: ' + str(self.client.email)

	client                    = models.ForeignKey('ptpgo.Clients') # Связь: Клиент
	photo                     = models.FileField(upload_to='client_photos/', blank=False, null=False) # Фотография
	timestamp                 = models.DateTimeField('added/updated', default=timezone.now) # Дата/время добавления фотографии



class ClientRatings(models.Model):

	class Meta:
		verbose_name_plural = "Клиенты: Рейтинг"

	def __str__(self):
		return self.client.email + ': ' + str(self.rating)

	client                    = models.ForeignKey('ptpgo.Clients') # Кому поставили рейтинг
	rating                    = models.FloatField(default=0.0) # Значение рейтинга (1-5)
	rated_by                  = models.IntegerField(default=0) # Кто поставил рейтинг
	timestamp                 = models.DateTimeField('added', default=timezone.now) # Когда поставили рейтинг



class ClientSiteNotifications(models.Model):

	class Meta:
		verbose_name_plural = "Клиенты: Уведомления на сайте"

	def __str__(self):
		return self.notification_type + ' | client: ' + self.client.email

	client                    = models.ForeignKey('ptpgo.Clients') # Связь: Клиент
	notification_type         = models.CharField(max_length=255) # Тип уведомления
	notification_data         = models.CharField(max_length=255) # Содержание уведомления
	checked                   = models.BooleanField(default=False) # Просмотрено ли уведомление
	timestamp                 = models.DateTimeField('added', default=timezone.now) # Дата/время, когда уведомление появилось



class ClientNotificationsLog(models.Model):

	class Meta:
		verbose_name_plural = "Клиенты: Лог sms и email уведомлений"

	def __str__(self):
		return self.destination_system + ' | client: ' + self.client.email

	client                    = models.ForeignKey('ptpgo.Clients') # Связь: Клиент
	notification_type         = models.CharField(max_length=255) # Тип уведомления
	notification_data         = models.CharField(max_length=255) # Содержание уведомления
	destination_system        = models.CharField(max_length=255) # Куда было направлено (сайт, email, sms)
	destination_details       = models.CharField(max_length=255) # Данные получателя
	timestamp                 = models.DateTimeField('added', default=timezone.now) # Дата/время уведомления



#######################################################################
#######################################################################
#######################################################################



class ListBoat(models.Model):

	class Meta:
		verbose_name_plural = 'Объявления: Водный транспорт'

	def __str__(self):
		return 'ID: ' + str(self.id) + ' | by ' + self.client.email

	client                    = models.ForeignKey('ptpgo.Clients') # Связь: Клиент

	boat_type                 = models.CharField(max_length=255, blank=True, null=True) # Тип транспорта
	boat_builder              = models.CharField(max_length=255, blank=True, null=True) # Производитель транспорта
	boat_model                = models.CharField(max_length=255, blank=True, null=True) # Модель транспорта
	boat_length               = models.CharField(max_length=255, blank=True, null=True) # Длина транспорта
	boat_build_year           = models.CharField(max_length=32) # Год производства

	location                  = models.CharField(max_length=1000, blank=True, null=True) # Текущее местоположение

	description               = models.CharField(max_length=10000, blank=True, null=True) # Описание транспорта
	amenities                 = models.CharField(max_length=10000, blank=True, null=True) # Удобства в свободной форме

	guest_capacity            = models.IntegerField(default=0) # Количество людей (гостей)
	cabins                    = models.IntegerField(default=0) # Количество кабин
	single_beds               = models.IntegerField(default=0) # Количество односпальных кроватей
	double_beds               = models.IntegerField(default=0) # Количество двуспальных кроватей

	engines_amount            = models.IntegerField(default=0) # Количество моторов
	horsepower_per_engine     = models.CharField(max_length=32, blank=True, null=True) # Лошадиных сил на мотор
	speed_per_hour            = models.CharField(max_length=32, blank=True, null=True) # Скорость в час

	avail_date_ranges         = models.CharField(max_length=1000, blank=True, null=True) # Доступные диапазоны дат в UTC

	with_captain              = models.BooleanField(default=True) # С капитаном
	fuel_included             = models.BooleanField(default=True) # Топливо включено

	#
	# место для хранения цен
	#

	canceled                  = models.BooleanField(default=False) # Объявление отменено

	timestamp_edited          = models.DateTimeField('date updated', default=timezone.now) # Дата/время редактирования
	timestamp_added           = models.DateTimeField('date listed', default=timezone.now) # Дата/время добавления



class ListBoatPhotos(models.Model):

	class Meta:
		verbose_name_plural = 'Объявления: Водный транспорт - фотографии'

	def __str__(self):
		return 'Объявление id: ' + str(self.boat.id)

	boat                      = models.ForeignKey('ptpgo.ListBoat') # Связь: Объявление - водный транспорт
	photo                     = models.FileField(upload_to='boat_photos/', blank=False, null=False) # Фотография
	timestamp                 = models.DateTimeField('added', default=timezone.now) # Дата/время добавления фотографии




class OrderBoat(models.Model):

	class Meta:
		verbose_name_plural = 'Заказы: Аренда водного транспорта'

	def __str__(self):
		return 'Номер заказа: ' + str(self.id) + '  |  Клиент: ' + self.client.email

	# ID этой модели: номер заказа
	client                    = models.ForeignKey('ptpgo.Clients') # Связь: Клиент
	boat                      = models.ForeignKey('ptpgo.ListBoat') # Связь: Объявление - водный транспорт
	date_range_selected       = models.CharField(max_length=1000) # Выбранные диапазоны дат в UTC

	# Статус заказа:
	# 	Принят в обработку
	# 	Отменен владельцем
	# 	Отменен заказчиком
	# 	Арендован
	# 	Сделка завершена
	# 	Сделка провалена
	status_order              = models.CharField(max_length=255)

	# Статус оплаты:
	# 	Не оплачено
	# 	Оплачено
	# 	Заказан возврат средств
	# 	Возврат средств подтвержден владельцем
	# 	Средства возвращены
	status_payment            = models.CharField(max_length=255)

	status_cancel_reason      = models.CharField(max_length=1000, blank=True, null=True) # Причина отмены заказа (владельцем или заказчиком)
	status_fail_reason        = models.CharField(max_length=1000, blank=True, null=True) # Причина провала, если указана (владельцем)

	timestamp                 = models.DateTimeField('order date/time', default=timezone.now) # Дата/время заказа



class Reviews(models.Model):

	class Meta:
		verbose_name_plural = 'Заказы: Отзывы по сделке'

	def __str__(self):
		return 'Отзыв от: ' + self.client.email

	client                    = models.ForeignKey('ptpgo.Clients') # Связь: Клиент, кто делает отзыв
	review_for                = models.IntegerField(default=0) # ID пользователя, которому пишут отзыв

	content                   = models.CharField(max_length=10000) # Содержимое отзыва

	timestamp                 = models.DateTimeField('review added date/time', default=timezone.now) # Дата/время добавления отзыва



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

	id_car_mark               = models.IntegerField(default=0) # ID марки
	name                      = models.CharField(max_length=255) # Название марки
	name_rus                  = models.CharField(max_length=255, blank=True, null=True) # Название марки на русском

	id_car_type               = models.ForeignKey('ptpgo.CarType') # Связь: Вид транспорта



# Модель автомобиля
class CarModel(models.Model):

	class Meta:
		verbose_name_plural = 'База авто: Модель автомобиля'

	def __str__(self):
		return self.name

	id_car_model              = models.IntegerField(default=0) # ID модели
	name                      = models.CharField(max_length=255) # Название модели
	name_rus                  = models.CharField(max_length=255, blank=True, null=True) # Название модели на русском

	id_car_mark               = models.IntegerField(default=0) # Связь: Марка автомобиля



# Поколение моделей
class CarGeneration(models.Model):

	class Meta:
		verbose_name_plural = 'База авто: Поколение моделей'

	def __str__(self):
		return self.name

	id_car_generation         = models.IntegerField(default=0) # ID поколения
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

	id_car_serie              = models.IntegerField(default=0) # ID серии
	name                      = models.CharField(max_length=255) # Название

	id_car_model              = models.IntegerField(default=0) # Связь: Модель автомобиля
	id_car_generation         = models.IntegerField(blank=True, null=True) # Связь: Поколение моделей



# Модификация автомобиля
class CarModification(models.Model):

	class Meta:
		verbose_name_plural = 'База авто: Модификация автомобиля'

	def __str__(self):
		return self.name

	id_car_modification       = models.IntegerField(default=0) # ID модификации
	name                      = models.CharField(max_length=255) # Название

	start_production_year     = models.IntegerField(blank=True, null=True) # Год начала производства
	end_production_year       = models.IntegerField(blank=True, null=True) # Год окончания производства
	price_min                 = models.IntegerField(blank=True, null=True) # Минимальная цена
	price_max                 = models.IntegerField(blank=True, null=True) # Максимальная цена

	id_car_model              = models.IntegerField(default=0) # Связь: Модель автомобиля
	id_car_serie              = models.IntegerField(default=0) # Связь: Серия автомобиля



# Значение характеристик автомобиля
class CarCharacteristicValue(models.Model):

	class Meta:
		verbose_name_plural = 'База авто: Значение характеристик автомобиля'

	def __str__(self):
		return 'ID названия характеристики: ' + str(self.id_car_characteristic) + ' | Модификация id: ' + str(self.id_car_modification)

	id_car_characteristic_value = models.IntegerField(default=0) # ID значения характеристики
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

	id_car_characteristic     = models.IntegerField(default=0) # ID названия характеристики
	name                      = models.CharField(max_length=255, blank=True, null=True) # Название
	parent                    = models.IntegerField(blank=True, null=True) # ID родительской характеристики

