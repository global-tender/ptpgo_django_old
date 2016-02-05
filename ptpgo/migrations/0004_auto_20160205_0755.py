# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-02-05 07:55
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('ptpgo', '0003_auto_20160205_0755'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clientphotos',
            name='updated',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='updated'),
        ),
        migrations.AlterField(
            model_name='clientratings',
            name='updated',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='updated'),
        ),
        migrations.AlterField(
            model_name='clients',
            name='registered',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='registered'),
        ),
        migrations.AlterField(
            model_name='clients',
            name='updated',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='updated'),
        ),
        migrations.AlterField(
            model_name='tokens',
            name='last_activity',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='last activity'),
        ),
        migrations.AlterField(
            model_name='tokens',
            name='last_login',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='last login'),
        ),
    ]