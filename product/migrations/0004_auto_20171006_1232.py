# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('product', '0003_adaptorproduct_type'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='adaptorproduct',
            options={'ordering': ('-date',)},
        ),
        migrations.AddField(
            model_name='adaptorattendcy',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True),
        ),
    ]
