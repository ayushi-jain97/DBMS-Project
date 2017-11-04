# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Memberphone',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('phone', models.IntegerField()),
            ],
            options={
                'db_table': 'memberPhone',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Members',
            fields=[
                ('rollnumber', models.IntegerField(serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('branch', models.CharField(max_length=20)),
                ('emailid', models.CharField(max_length=50, db_column=b'emailID')),
            ],
            options={
                'db_table': 'members',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Postdesc',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('designation', models.CharField(max_length=20)),
                ('serviceYear', models.IntegerField(db_column=b'serviceYear')),
                ('category', models.CharField(max_length=20)),
            ],
            options={
                'db_table': 'postDesc',
                'managed': False,
            },
        ),
    ]
