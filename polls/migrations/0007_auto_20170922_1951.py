# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-22 17:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0006_auto_20170921_0038'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='choice',
            name='question',
        ),
        migrations.RenameField(
            model_name='plate',
            old_name='name',
            new_name='spz',
        ),
        migrations.AddField(
            model_name='plate',
            name='corrSpz',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.DeleteModel(
            name='Choice',
        ),
        migrations.DeleteModel(
            name='Question',
        ),
    ]