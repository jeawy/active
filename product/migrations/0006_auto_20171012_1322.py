# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0005_auto_20171006_1505'),
    ]

    operations = [
        migrations.CreateModel(
            name='DetailPic',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('url', models.CharField(max_length=4096)),
                ('name', models.CharField(default=b'', max_length=4096)),
                ('ref', models.SmallIntegerField(default=0)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AlterModelTable(
            name='productpic',
            table='productpic',
        ),
    ]
