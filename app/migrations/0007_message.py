# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-03-06 20:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_auto_20160306_1918'),
    ]

    operations = [
        migrations.CreateModel(
            name='message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('receiver', models.CharField(max_length=30)),
                ('sender', models.CharField(max_length=30)),
                ('msg', models.CharField(max_length=1000)),
            ],
        ),
    ]