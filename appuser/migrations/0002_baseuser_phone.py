# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appuser', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='baseuser',
            name='phone',
            field=models.CharField(max_length=128, null=True, verbose_name='\u7535\u8bdd'),
        ),
    ]
