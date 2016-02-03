# -*- coding: utf-8 -*-
import datetime
from django.db import models

class Clients(models.Model):

	class Meta:
		verbose_name_plural = 'Clients'

	def __unicode__(self):
		return self.email + '; id: ' + str(self.id)


	email                     = models.CharField(max_length=100)
	password                  = models.CharField(max_length=1000)

	fio                       = models.CharField(max_length=1000)
	about                     = models.CharField(max_length=10000)

	country                   = models.ForeignKey('ptpgo.Country')
	city                      = models.ForeignKey('ptpgo.City')

	phone                     = models.CharField(max_length=1000)
	additional_contacts       = models.CharField(max_length=1000)

	photo                     = models.ForeignKey('ptpgo.ClientPhotos')
	rating                    = models.ForeignKey('ptpgo.ClientRatings')

	registered                = models.DateTimeField('registered', default=datetime.datetime.now)
	updated                   = models.DateTimeField('updated', default=datetime.datetime.now)

class Tokens(models.Model):

	class Meta:
		verbose_name_plural = "Tokens"

	def __unicode__(self):
		return self.client.email + ': ' + self.token

	client                    = models.ForeignKey('ptpgo.Clients')
	token                     = models.CharField(max_length=1000)
	last_login                = models.DateTimeField('last login', default=datetime.datetime.now)
	last_activity             = models.DateTimeField('last activity', default=datetime.datetime.now)

class ClientPhotos(models.Model):

	class Meta:
		verbose_name_plural = "ClientPhotos"

	def __unicode__(self):
		return 'id: ' + str(self.id) + '; client: ' + str(self.client.email)

	client                    = models.ForeignKey('ptpgo.Clients')
	photo                     = models.FileField(upload_to='client_photos/', blank=False, null=False)
	updated                   = models.DateTimeField('updated', default=datetime.datetime.now)

class ClientRatings(models.Model):

	class Meta:
		verbose_name_plural = "ClientRatings"

	def __unicode__(self):
		return self.client.email + ': ' + str(self.rating)

	client                    = models.ForeignKey('ptpgo.Clients')
	rating                    = models.FloatField(default=0.0)
	updated                   = models.DateTimeField('updated', default=datetime.datetime.now)

class Country(models.Model):

	class Meta:
		verbose_name_plural = "Countries"

	def __unicode__(self):
		return str(self.id)

class City(models.Model):

	class Meta:
		verbose_name_plural = "Cities"

	def __unicode__(self):
		return str(self.id)