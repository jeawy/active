# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0004_auto_20171006_1232'),
    ]

    operations = [
        migrations.AddField(
            model_name='adaptorproduct',
            name='set_grid',
            field=models.SmallIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='adaptorproduct',
            name='set_homepage',
            field=models.SmallIntegerField(default=0),
        ),
    ]
