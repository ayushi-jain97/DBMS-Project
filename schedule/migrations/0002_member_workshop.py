# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Member',
            fields=[
                ('rollnumber', models.IntegerField(serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('branch', models.CharField(max_length=20)),
                ('emailID', models.CharField(max_length=50, db_column=b'emailID')),
            ],
            options={
                'db_table': 'members',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Workshop',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateField()),
                ('time', models.CharField(max_length=10)),
                ('venue', models.CharField(max_length=20)),
                ('topic', models.CharField(max_length=40, null=True, blank=True)),
                ('level', models.CharField(max_length=40, null=True, blank=True)),
                ('targetAudience', models.CharField(max_length=40, null=True, db_column=b'targetAudience', blank=True)),
                ('text', models.CharField(max_length=200, null=True, blank=True)),
            ],
            options={
                'db_table': 'workshops',
                'managed': False,
            },
        ),
    ]
