from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver


class Clients(models.Model):

    class Meta:
        verbose_name_plural = 'Клиенты: Данные клиента'

    def __str__(self):
        return 'id: ' + str(self.id) + '; user: ' + str(self.user.email)

    user                        = models.ForeignKey(User)

    vk_user_id                  = models.CharField(max_length=255, blank=True, null=True)
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


class ClientPhotos(models.Model):

    class Meta:
        verbose_name_plural = "Клиенты: Фотографии"

    def __str__(self):
        return 'id: ' + str(self.id) + '; user: ' + str(self.user.email)

    user                      = models.ForeignKey(User) # Связь: Пользователь
    photo                     = models.FileField(upload_to='client_photos/', blank=False, null=False) # Фотография
    timestamp                 = models.DateTimeField('added/updated', default=timezone.now) # Дата/время добавления фотографии


class ClientRatings(models.Model):

    class Meta:
        verbose_name_plural = "Клиенты: Рейтинг"

    def __str__(self):
        return self.user.email + ': ' + str(self.rating)

    user                      = models.ForeignKey(User) # Кому поставили рейтинг
    rating                    = models.FloatField(default=0.0) # Значение рейтинга (1-5)
    rated_by                  = models.IntegerField(default=0) # Кто поставил рейтинг
    timestamp                 = models.DateTimeField('added', default=timezone.now) # Когда поставили рейтинг


class ClientSiteNotifications(models.Model):

    class Meta:
        verbose_name_plural = "Клиенты: Уведомления на сайте"

    def __str__(self):
        return self.notification_type + ' | user: ' + self.user.email

    user                      = models.ForeignKey(User) # Связь: Пользователь
    notification_type         = models.CharField(max_length=255) # Тип уведомления
    notification_data         = models.CharField(max_length=255) # Содержание уведомления
    checked                   = models.BooleanField(default=False) # Просмотрено ли уведомление
    timestamp                 = models.DateTimeField('added', default=timezone.now) # Дата/время, когда уведомление появилось


class ClientNotificationsLog(models.Model):

    class Meta:
        verbose_name_plural = "Клиенты: Лог sms и email уведомлений"

    def __str__(self):
        return self.destination_system + ' | user: ' + self.user.email

    user                      = models.ForeignKey(User) # Связь: Пользователь
    notification_type         = models.CharField(max_length=255) # Тип уведомления
    notification_data         = models.CharField(max_length=255) # Содержание уведомления
    destination_system        = models.CharField(max_length=255) # Куда было направлено (email, sms)
    destination_details       = models.CharField(max_length=255) # Данные получателя
    timestamp                 = models.DateTimeField('added', default=timezone.now) # Дата/время уведомления


# Receive the pre_delete signal and delete the file associated with the model instance.
@receiver(pre_delete, sender=ClientPhotos)
def clientphotos_delete(sender, instance, **kwargs):
    # Pass false so FileField doesn't save the model.
    instance.photo.delete(False)