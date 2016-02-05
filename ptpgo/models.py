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

