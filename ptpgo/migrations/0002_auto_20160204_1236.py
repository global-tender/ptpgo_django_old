# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-02-04 12:36
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ptpgo', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='city',
            options={'verbose_name_plural': 'Cities'},
        ),
        migrations.AlterModelOptions(
            name='clientphotos',
            options={'verbose_name_plural': 'ClientPhotos'},
        ),
        migrations.AlterModelOptions(
            name='clientratings',
            options={'verbose_name_plural': 'ClientRatings'},
        ),
        migrations.AlterModelOptions(
            name='clients',
            options={'verbose_name_plural': 'Clients'},
        ),
        migrations.AlterModelOptions(
            name='country',
            options={'verbose_name_plural': 'Countries'},
        ),
        migrations.AlterModelOptions(
            name='tokens',
            options={'verbose_name_plural': 'Tokens'},
        ),
        migrations.AlterField(
            model_name='clients',
            name='about',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='clients',
            name='additional_contacts',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name='clients',
            name='city',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='ptpgo.City'),
        ),
        migrations.AlterField(
            model_name='clients',
            name='country',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='ptpgo.Country'),
        ),
        migrations.AlterField(
            model_name='clients',
            name='fio',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name='clients',
            name='phone',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name='clients',
            name='photo',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='ptpgo.ClientPhotos'),
        ),
        migrations.AlterField(
            model_name='clients',
            name='rating',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='ptpgo.ClientRatings'),
        ),
    ]
