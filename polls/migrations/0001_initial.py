# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-19 19:09
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Choice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('choice_text', models.CharField(max_length=200)),
                ('votes', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Plate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('cap_date', models.DateTimeField(verbose_name='date captured')),
                ('image', models.ImageField(upload_to='images/plates')),
                ('corr', models.ImageField(blank=True, upload_to='images/corrected')),
                ('arr_dep', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question_text', models.CharField(max_length=200)),
                ('pub_date', models.DateTimeField(verbose_name='date published')),
            ],
        ),
        migrations.CreateModel(
            name='Visitor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('spz', models.CharField(max_length=10)),
                ('reg_date', models.DateTimeField(verbose_name='date registrated')),
                ('last_visit_date', models.DateTimeField(verbose_name='date visited')),
                ('comment', models.CharField(max_length=500)),
                ('profile_image', models.ImageField(upload_to='images/profile_pics/')),
                ('allowed_date_from', models.DateTimeField(blank=True, verbose_name='allowed_date_from')),
                ('allowed_date_to', models.DateTimeField(blank=True, verbose_name='allowed_date_to')),
                ('time_from', models.TimeField(blank=True, verbose_name='time_from')),
                ('time_to', models.TimeField(blank=True, verbose_name='time_to')),
            ],
        ),
        migrations.AddField(
            model_name='plate',
            name='visitor',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='polls.Visitor'),
        ),
        migrations.AddField(
            model_name='choice',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='polls.Question'),
        ),
    ]
