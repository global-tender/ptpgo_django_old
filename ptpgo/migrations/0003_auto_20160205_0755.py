# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-02-05 07:55
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('ptpgo', '0002_auto_20160204_1236'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clientphotos',
            name='updated',
            field=models.DateTimeField(default=datetime.datetime(2016, 2, 5, 7, 55, 0, 182292, tzinfo=utc), verbose_name='updated'),
        ),
        migrations.AlterField(
            model_name='clientratings',
            name='updated',
            field=models.DateTimeField(default=datetime.datetime(2016, 2, 5, 7, 55, 0, 183273, tzinfo=utc), verbose_name='updated'),
        ),
        migrations.AlterField(
            model_name='clients',
            name='registered',
            field=models.DateTimeField(default=datetime.datetime(2016, 2, 5, 7, 55, 0, 179410, tzinfo=utc), verbose_name='registered'),
        ),
        migrations.AlterField(
            model_name='clients',
            name='updated',
            field=models.DateTimeField(default=datetime.datetime(2016, 2, 5, 7, 55, 0, 179507, tzinfo=utc), verbose_name='updated'),
        ),
        migrations.AlterField(
            model_name='tokens',
            name='last_activity',
            field=models.DateTimeField(default=datetime.datetime(2016, 2, 5, 7, 55, 0, 181343, tzinfo=utc), verbose_name='last activity'),
        ),
        migrations.AlterField(
            model_name='tokens',
            name='last_login',
            field=models.DateTimeField(default=datetime.datetime(2016, 2, 5, 7, 55, 0, 181293, tzinfo=utc), verbose_name='last login'),
        ),
    ]