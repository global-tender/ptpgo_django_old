# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-02-05 12:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ptpgo', '0004_auto_20160205_0755'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='clients',
            name='city',
        ),
        migrations.RemoveField(
            model_name='clients',
            name='country',
        ),
        migrations.RemoveField(
            model_name='clients',
            name='photo',
        ),
        migrations.RemoveField(
            model_name='clients',
            name='rating',
        ),
        migrations.AddField(
            model_name='clients',
            name='confirm_code',
            field=models.CharField(blank=True, default='', max_length=1000, null=True),
        ),
        migrations.AddField(
            model_name='tokens',
            name='device_info',
            field=models.CharField(blank=True, default='', max_length=1000, null=True),
        ),
        migrations.DeleteModel(
            name='City',
        ),
        migrations.DeleteModel(
            name='Country',
        ),
    ]