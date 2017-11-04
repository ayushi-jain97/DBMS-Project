# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('register', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Participant',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('college', models.CharField(max_length=100)),
                ('email', models.CharField(max_length=50)),
                ('phone', models.IntegerField()),
                ('username', models.CharField(max_length=30)),
                ('password', models.CharField(max_length=50)),
                ('gender', models.CharField(max_length=10)),
            ],
            options={
                'db_table': 'participants',
                'managed': False,
            },
        ),
    ]
