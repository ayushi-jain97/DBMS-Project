# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Merchandise',
            fields=[
                ('itemid', models.AutoField(serialize=False, primary_key=True)),
                ('image', models.CharField(max_length=100)),
                ('type', models.CharField(max_length=20)),
                ('price', models.IntegerField()),
                ('text', models.CharField(max_length=200, null=True, blank=True)),
            ],
            options={
                'db_table': 'merchandise',
                'managed': False,
            },
        ),
    ]
