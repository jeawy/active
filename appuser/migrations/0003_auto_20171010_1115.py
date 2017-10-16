# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appuser', '0002_baseuser_phone'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='baseuser',
            options={'permissions': (('admin_management', 'manage group, permission and user'), ('staff', 'Check attendecies.'))},
        ),
        migrations.AddField(
            model_name='baseuser',
            name='is_staff',
            field=models.BooleanField(default=False, verbose_name='\u53ea\u53ef\u4ee5\u67e5\u770b\u6d3b\u52a8\u7684\u5458\u5de5'),
        ),
    ]
