# -*- coding: utf-8 -*-
# Generated by Django 1.11.14 on 2018-11-01 14:50
from __future__ import unicode_literals

import accounts.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0008_alter_user_username_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('picture', models.ImageField(blank=True, default='user_picture/default.jpg', upload_to=accounts.models.user_picture, verbose_name='头像')),
            ],
        ),
    ]
