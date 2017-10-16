# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0006_auto_20171012_1322'),
    ]

    operations = [
        migrations.AlterField(
            model_name='adaptorproduct',
            name='datefrom',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='adaptorproduct',
            name='dateto',
            field=models.DateTimeField(null=True),
        ),
    ]
