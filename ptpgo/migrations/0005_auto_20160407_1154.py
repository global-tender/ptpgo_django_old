# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-04-07 11:54
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('ptpgo', '0004_auto_20160406_1150'),
    ]

    operations = [
        migrations.CreateModel(
            name='ListBoat',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('boat_type', models.CharField(blank=True, max_length=255, null=True)),
                ('boat_builder', models.CharField(blank=True, max_length=255, null=True)),
                ('boat_model', models.CharField(blank=True, max_length=255, null=True)),
                ('boat_length', models.CharField(blank=True, max_length=255, null=True)),
                ('boat_build_year', models.CharField(max_length=32)),
                ('location', models.CharField(blank=True, max_length=1000, null=True)),
                ('description', models.CharField(blank=True, max_length=10000, null=True)),
                ('amenities', models.CharField(blank=True, max_length=10000, null=True)),
                ('guest_capacity', models.IntegerField(default=0)),
                ('cabins', models.IntegerField(default=0)),
                ('single_beds', models.IntegerField(default=0)),
                ('double_beds', models.IntegerField(default=0)),
                ('engines_amount', models.IntegerField(default=0)),
                ('horsepower_per_engine', models.CharField(blank=True, max_length=32, null=True)),
                ('speed_per_hour', models.CharField(blank=True, max_length=32, null=True)),
                ('avail_date_ranges', models.CharField(blank=True, max_length=1000, null=True)),
                ('with_captain', models.BooleanField(default=True)),
                ('fuel_included', models.BooleanField(default=True)),
                ('canceled', models.BooleanField(default=False)),
                ('timestamp_edited', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date updated')),
                ('timestamp_added', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date listed')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Объявления: Водный транспорт',
            },
        ),
        migrations.CreateModel(
            name='ListBoatPhotos',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('photo', models.FileField(upload_to='boat_photos/')),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now, verbose_name='added')),
                ('boat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ptpgo.ListBoat')),
            ],
            options={
                'verbose_name_plural': 'Объявления: Водный транспорт - фотографии',
            },
        ),
        migrations.CreateModel(
            name='OrderBoat',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_range_selected', models.CharField(max_length=1000)),
                ('status_order', models.CharField(max_length=255)),
                ('status_payment', models.CharField(max_length=255)),
                ('status_cancel_reason', models.CharField(blank=True, max_length=1000, null=True)),
                ('status_fail_reason', models.CharField(blank=True, max_length=1000, null=True)),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now, verbose_name='order date/time')),
                ('boat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ptpgo.ListBoat')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Заказы: Аренда водного транспорта',
            },
        ),
        migrations.CreateModel(
            name='Reviews',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('review_for', models.IntegerField(default=0)),
                ('content', models.CharField(max_length=10000)),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now, verbose_name='review added date/time')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Заказы: Отзывы по сделке',
            },
        ),
        migrations.AlterModelOptions(
            name='clients',
            options={'verbose_name_plural': 'Клиенты: Клиент'},
        ),
    ]
