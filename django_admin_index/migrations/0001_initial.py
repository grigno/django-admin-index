# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-02 08:40
from __future__ import unicode_literals

import django.contrib.contenttypes.models
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='AppGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.PositiveIntegerField(db_index=True, editable=False)),
                ('name', models.CharField(max_length=200, verbose_name='name')),
                ('slug', models.SlugField(unique=True, verbose_name='slug')),
            ],
            options={
                'verbose_name_plural': 'application groups',
                'verbose_name': 'application group',
                'abstract': False,
                'ordering': ('order',),
            },
        ),
        migrations.CreateModel(
            name='AppLink',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.PositiveIntegerField(db_index=True, editable=False)),
                ('name', models.CharField(max_length=200)),
                ('link', models.CharField(max_length=200)),
                ('app_group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='admin_index.AppGroup')),
            ],
            options={
                'verbose_name_plural': 'application links',
                'verbose_name': 'application link',
                'abstract': False,
                'ordering': ('order',),
            },
        ),
        migrations.CreateModel(
            name='ContentTypeProxy',
            fields=[
            ],
            options={
                'proxy': True,
                'ordering': ('app_label', 'model'),
            },
            bases=('contenttypes.contenttype',),
            managers=[
                ('objects', django.contrib.contenttypes.models.ContentTypeManager()),
            ],
        ),
        migrations.AddField(
            model_name='appgroup',
            name='models',
            field=models.ManyToManyField(blank=True, to='admin_index.ContentTypeProxy'),
        ),
    ]