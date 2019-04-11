# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2017-05-04 16:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('twittr', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='twitterprofile',
            old_name='profile_name',
            new_name='name',
        ),
        migrations.AlterField(
            model_name='twitterprofile',
            name='profile_pic',
            field=models.CharField(default='', max_length=200),
        ),
    ]
