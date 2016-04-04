from django.db import models
from django.contrib.auth.models import User


class Clients(models.Model):

    class Meta:
        verbose_name_plural = 'Клиенты: Данные клиента'

    def __str__(self):
        return str(self.user.id)

    user                        = models.ForeignKey(User)

    vk_token                    = models.CharField(max_length=255, blank=True, null=True)
    vk_extra_data               = models.CharField(max_length=10000, blank=True, null=True)

    about                       = models.TextField(blank=True, null=True) # О себе

    phone                       = models.CharField(max_length=255, blank=True, null=True) # Номер телефона, только цифры, без пробелов
    additional_contacts         = models.CharField(max_length=1000, blank=True, null=True) # Дополнительные контакты, в свободной форме

    email_confirmed             = models.BooleanField(default=False) # Был ли подтвержден E-Mail
    email_confirm_code          = models.CharField(max_length=255, blank=True, null=True) # Код потверждения E-Mail адреса

    phone_confirmed             = models.BooleanField(default=False) # Был ли подтвержден номер телефона
    phone_confirm_code          = models.CharField(max_length=255, blank=True, null=True) # Код потверждения номер телефона

    # Среднее время отклика на заказ, подсчитывается и изменяется по отклику
    response_time               = models.CharField(max_length=32, blank=True, null=True)
    # В процентах количество откликов на заказ (пример: 100%)
    response_rate               = models.CharField(max_length=32, blank=True, null=True)

    honors                      = models.IntegerField(default=0) # Награды - баллы







############################
############################
############################
# Вид транспорта
class CarType(models.Model):

    class Meta:
        verbose_name_plural = 'База авто: Вид транспорта'

    def __str__(self):
        return self.name

    name                        = models.CharField(max_length=255)  # пример: легковые


# Марка автомобиля
class CarMark(models.Model):

    class Meta:
        verbose_name_plural = 'База авто: Марка автомобиля'

    def __str__(self):
        return self.name

    id_car_mark                 = models.IntegerField(default=0)  # ID марки
    name                        = models.CharField(max_length=255)  # Название марки
    name_rus                    = models.CharField(max_length=255, blank=True, null=True)  # Название марки на русском

    id_car_type                 = models.ForeignKey('ptpgo.CarType')  # Связь: Вид транспорта


# Модель автомобиля
class CarModel(models.Model):

    class Meta:
        verbose_name_plural = 'База авто: Модель автомобиля'

    def __str__(self):
        return self.name

    id_car_model                = models.IntegerField(default=0)  # ID модели
    name                        = models.CharField(max_length=255)  # Название модели
    name_rus                    = models.CharField(max_length=255, blank=True, null=True)  # Название модели на русском

    id_car_mark                 = models.IntegerField(default=0)  # Связь: Марка автомобиля


# Поколение моделей
class CarGeneration(models.Model):

    class Meta:
        verbose_name_plural = 'База авто: Поколение моделей'

    def __str__(self):
        return self.name

    id_car_generation           = models.IntegerField(default=0)  # ID поколения
    name                        = models.CharField(max_length=255)  # Название
    year_begin                  = models.CharField(max_length=255, default="", blank=True, null=True)  # Год начала выпуска
    year_end                    = models.CharField(max_length=255, default="", blank=True, null=True)  # Год окончания выпуска

    id_car_model                = models.IntegerField(default=0)  # Связь: Модель автомобиля


# Серия автомобиля
class CarSerie(models.Model):

    class Meta:
        verbose_name_plural = 'База авто: Серия автомобиля'

    def __str__(self):
        return self.name

    id_car_serie                = models.IntegerField(default=0)  # ID серии
    name                        = models.CharField(max_length=255)  # Название

    id_car_model                = models.IntegerField(default=0)  # Связь: Модель автомобиля
    id_car_generation           = models.IntegerField(blank=True, null=True)  # Связь: Поколение моделей


# Модификация автомобиля
class CarModification(models.Model):

    class Meta:
        verbose_name_plural = 'База авто: Модификация автомобиля'

    def __str__(self):
        return self.name

    id_car_modification         = models.IntegerField(default=0)  # ID модификации
    name                        = models.CharField(max_length=255)  # Название

    start_production_year       = models.IntegerField(blank=True, null=True)  # Год начала производства
    end_production_year         = models.IntegerField(blank=True, null=True)  # Год окончания производства
    price_min                   = models.IntegerField(blank=True, null=True)  # Минимальная цена
    price_max                   = models.IntegerField(blank=True, null=True)  # Максимальная цена

    id_car_model                = models.IntegerField(default=0)  # Связь: Модель автомобиля
    id_car_serie                = models.IntegerField(default=0)  # Связь: Серия автомобиля


# Значение характеристик автомобиля
class CarCharacteristicValue(models.Model):

    class Meta:
        verbose_name_plural = 'База авто: Значение характеристик автомобиля'

    def __str__(self):
        return 'ID названия характеристики: ' + str(self.id_car_characteristic) + ' | Модификация id: ' + str(self.id_car_modification)

    id_car_characteristic_value = models.IntegerField(default=0)  # ID значения характеристики
    value                       = models.CharField(max_length=255)  # Значение
    unit                        = models.CharField(max_length=255, blank=True, null=True)  # Единица измерения

    id_car_characteristic       = models.IntegerField(default=0)  # Связь: Название характеристики
    id_car_modification         = models.IntegerField(default=0)  # Связь: Модификация автомобиля


# Название характеристики автомобиля
class CarCharacteristic(models.Model):

    class Meta:
        verbose_name_plural = 'База авто: Название характеристики'

    def __str__(self):
        return self.name

    id_car_characteristic       = models.IntegerField(default=0)  # ID названия характеристики
    name                        = models.CharField(max_length=255, blank=True, null=True)  # Название
    parent                      = models.IntegerField(blank=True, null=True)  # ID родительской характеристики
