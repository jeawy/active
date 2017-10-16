# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0002_remove_adaptorproduct_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='adaptorproduct',
            name='type',
            field=models.SmallIntegerField(default=1),
        ),
    ]
