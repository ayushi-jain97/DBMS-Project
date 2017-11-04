# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0002_member_workshop'),
    ]

    operations = [
        migrations.CreateModel(
            name='Workshops',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateField()),
                ('time', models.CharField(max_length=10)),
                ('venue', models.CharField(max_length=20)),
                ('topic', models.CharField(max_length=40, null=True, blank=True)),
                ('level', models.CharField(max_length=40, null=True, blank=True)),
                ('targetaudience', models.CharField(max_length=40, null=True, db_column=b'targetAudience', blank=True)),
                ('text', models.CharField(max_length=200, null=True, blank=True)),
            ],
            options={
                'db_table': 'workshops',
                'managed': False,
            },
        ),
    ]
