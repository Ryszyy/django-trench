# -*- coding: utf-8 -*-
# Generated by Django 1.11.18 on 2019-09-26 12:35
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('testapp', '0002_user_yubikey_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='yubikey_id',
        ),
    ]
