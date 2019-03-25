# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2019-03-23 00:09
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('my_wall', '0004_auto_20190322_1657'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='message',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='my_wall.Message'),
            preserve_default=False,
        ),
    ]
