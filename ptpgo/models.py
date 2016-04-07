from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver


class Clients(models.Model):

    class Meta:
        verbose_name_plural = 'Клиенты: Клиент'

    def __str__(self):
        return 'ID: ' + str(self.id) + ' | Пользователь: ' + self.user.email

    user                        = models.ForeignKey(User)

    vk_user_id                  = models.CharField(max_length=255, blank=True, null=True)
    vk_token                    = models.CharField(max_length=255, blank=True, null=True)
    vk_extra_data               = models.CharField(max_length=10000, blank=True, null=True)

    about                       = models.TextField(blank=True, null=True)  # О себе

    phone                       = models.CharField(max_length=255, blank=True, null=True)  # Номер телефона, только цифры, без пробелов
    additional_contacts         = models.CharField(max_length=1000, blank=True, null=True)  # Дополнительные контакты, в свободной форме

    email_confirmed             = models.BooleanField(default=False)  # Был ли подтвержден E-Mail
    email_confirm_code          = models.CharField(max_length=255, blank=True, null=True)  # Код потверждения E-Mail адреса

    phone_confirmed             = models.BooleanField(default=False)  # Был ли подтвержден номер телефона
    phone_confirm_code          = models.CharField(max_length=255, blank=True, null=True)  # Код потверждения номер телефона

    # Среднее время отклика на заказ, подсчитывается и изменяется по отклику
    response_time               = models.CharField(max_length=32, blank=True, null=True)
    # В процентах количество откликов на заказ (пример: 100%)
    response_rate               = models.CharField(max_length=32, blank=True, null=True)

    honors                      = models.IntegerField(default=0)  # Награды - баллы


class ClientPhotos(models.Model):

    class Meta:
        verbose_name_plural = "Клиенты: Фотографии"

    def __str__(self):
        return 'ID: ' + str(self.id) + ' | Пользователь: ' + self.user.email

    user                      = models.ForeignKey(User)  # Связь: Пользователь
    photo                     = models.FileField(upload_to='client_photos/', blank=False, null=False)  # Фотография
    timestamp                 = models.DateTimeField('added/updated', default=timezone.now)  # Дата/время добавления фотографии


class ClientRatings(models.Model):

    class Meta:
        verbose_name_plural = "Клиенты: Рейтинг"

    def __str__(self):
        return 'ID: ' + str(self.id) + ' | Пользователь: ' + self.user.email

    user                      = models.ForeignKey(User)  # Кому поставили рейтинг
    rating                    = models.FloatField(default=0.0)  # Значение рейтинга (1-5)
    rated_by                  = models.IntegerField(default=0)  # Кто поставил рейтинг
    timestamp                 = models.DateTimeField('added', default=timezone.now)  # Когда поставили рейтинг


class ClientSiteNotifications(models.Model):

    class Meta:
        verbose_name_plural = "Клиенты: Уведомления на сайте"

    def __str__(self):
        return 'ID: ' + str(self.id) + ' | Пользователь: ' + self.user.email

    user                      = models.ForeignKey(User)  # Связь: Пользователь
    notification_type         = models.CharField(max_length=255)  # Тип уведомления
    notification_data         = models.CharField(max_length=255)  # Содержание уведомления
    checked                   = models.BooleanField(default=False)  # Просмотрено ли уведомление
    timestamp                 = models.DateTimeField('added', default=timezone.now)  # Дата/время, когда уведомление появилось


class ClientNotificationsLog(models.Model):

    class Meta:
        verbose_name_plural = "Клиенты: Лог sms и email уведомлений"

    def __str__(self):
        return 'ID: ' + str(self.id) + ' | Пользователь: ' + self.user.email

    user                      = models.ForeignKey(User)  # Связь: Пользователь
    notification_type         = models.CharField(max_length=255)  # Тип уведомления
    notification_data         = models.CharField(max_length=255)  # Содержание уведомления
    destination_system        = models.CharField(max_length=255)  # Куда было направлено (email, sms)
    destination_details       = models.CharField(max_length=255)  # Данные получателя
    timestamp                 = models.DateTimeField('added', default=timezone.now)  # Дата/время уведомления


#######################################################################
#######################################################################
#######################################################################


class ListBoat(models.Model):

    class Meta:
        verbose_name_plural = 'Объявления: Водный транспорт'

    def __str__(self):
        return 'ID: ' + str(self.id) + ' | Пользователь: ' + self.user.email

    user                      = models.ForeignKey(User) # Связь: Пользователь

    boat_type                 = models.CharField(max_length=255, blank=True, null=True)  # Тип транспорта
    boat_builder              = models.CharField(max_length=255, blank=True, null=True)  # Производитель транспорта
    boat_model                = models.CharField(max_length=255, blank=True, null=True)  # Модель транспорта
    boat_length               = models.CharField(max_length=255, blank=True, null=True)  # Длина транспорта
    boat_build_year           = models.CharField(max_length=32)  # Год производства

    location                  = models.CharField(max_length=1000, blank=True, null=True)  # Текущее местоположение

    description               = models.CharField(max_length=10000, blank=True, null=True)  # Описание транспорта
    amenities                 = models.CharField(max_length=10000, blank=True, null=True)  # Удобства в свободной форме

    guest_capacity            = models.IntegerField(default=0)  # Количество людей (гостей)
    cabins                    = models.IntegerField(default=0)  # Количество кабин
    single_beds               = models.IntegerField(default=0)  # Количество односпальных кроватей
    double_beds               = models.IntegerField(default=0)  # Количество двуспальных кроватей

    engines_amount            = models.IntegerField(default=0)  # Количество моторов
    horsepower_per_engine     = models.CharField(max_length=32, blank=True, null=True)  # Лошадиных сил на мотор
    speed_per_hour            = models.CharField(max_length=32, blank=True, null=True)  # Скорость в час

    avail_date_ranges         = models.CharField(max_length=1000, blank=True, null=True)  # Доступные диапазоны дат в UTC

    with_captain              = models.BooleanField(default=True)  # С капитаном
    fuel_included             = models.BooleanField(default=True)  # Топливо включено

    # место для хранения цен

    canceled                  = models.BooleanField(default=False)  # Объявление отменено

    timestamp_edited          = models.DateTimeField('date updated', default=timezone.now)  # Дата/время редактирования
    timestamp_added           = models.DateTimeField('date listed', default=timezone.now)  # Дата/время добавления


class ListBoatPhotos(models.Model):

    class Meta:
        verbose_name_plural = 'Объявления: Водный транспорт - фотографии'

    def __str__(self):
        return 'ID: ' + str(self.id) + ' | Объявление: ' + str(self.boat.id)

    boat                      = models.ForeignKey('ptpgo.ListBoat')  # Связь: Объявления - водный транспорт
    photo                     = models.FileField(upload_to='boat_photos/', blank=False, null=False)  # Фотография
    timestamp                 = models.DateTimeField('added', default=timezone.now)  # Дата/время добавления фотографии


class OrderBoat(models.Model):

    class Meta:
        verbose_name_plural = 'Заказы: Аренда водного транспорта'

    def __str__(self):
        return 'Номер заказа: ' + str(self.id) + ' | Пользователь: ' + self.user.email

    # ID этой модели: номер заказа
    user                      = models.ForeignKey(User)  # Связь: Пользователь
    boat                      = models.ForeignKey('ptpgo.ListBoat')  # Связь: Объявление - водный транспорт
    date_range_selected       = models.CharField(max_length=1000)  # Выбранные диапазоны дат в UTC

    # Статус заказа:
    #   Принят в обработку
    #   Отменен владельцем
    #   Отменен заказчиком
    #   Арендован
    #   Сделка завершена
    #   Сделка провалена
    status_order              = models.CharField(max_length=255)

    # Статус оплаты:
    #   Не оплачено
    #   Оплачено
    #   Заказан возврат средств
    #   Возврат средств подтвержден владельцем
    #   Средства возвращены
    status_payment            = models.CharField(max_length=255)

    status_cancel_reason      = models.CharField(max_length=1000, blank=True, null=True)  # Причина отмены заказа (владельцем или заказчиком)
    status_fail_reason        = models.CharField(max_length=1000, blank=True, null=True)  # Причина провала, если указана (владельцем)

    timestamp                 = models.DateTimeField('order date/time', default=timezone.now)  # Дата/время заказа



class Reviews(models.Model):

    class Meta:
        verbose_name_plural = 'Заказы: Отзывы по сделке'

    def __str__(self):
        return 'ID: ' + str(self.id) + ' | Пользователь: ' + str(self.user.email)

    user                      = models.ForeignKey(User)  # Связь: Пользователь, кто делает отзыв
    review_for                = models.IntegerField(default=0)  # ID пользователя, которому пишут отзыв

    content                   = models.CharField(max_length=10000)  # Содержимое отзыва

    timestamp                 = models.DateTimeField('review added date/time', default=timezone.now)  # Дата/время добавления отзыва


# Receive the pre_delete signal and delete the file associated with the model instance.
@receiver(pre_delete, sender=ClientPhotos)
def clientphotos_delete(sender, instance, **kwargs):
    # Pass false so FileField doesn't save the model.
    instance.photo.delete(False)

@receiver(pre_delete, sender=ListBoatPhotos)
def listboatphotos_delete(sender, instance, **kwargs):
    # Pass false so FileField doesn't save the model.
    instance.photo.delete(False)