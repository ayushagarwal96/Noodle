# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-25 19:17
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0009_book_edition'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='book',
            name='seller',
        ),
    ]
