# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-24 19:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0002_auto_20170324_2342'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='cover',
            field=models.CharField(default='self.title', max_length=1000),
            preserve_default=False,
        ),
    ]
