# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AdaptorAttendcy',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=1024, null=True, verbose_name='name')),
                ('phone', models.CharField(default=b'', max_length=4096, verbose_name='phone')),
                ('quantity', models.PositiveIntegerField(default=0, null=True, verbose_name='inventory')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='AdaptorProduct',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('modify_date', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=2048, verbose_name='title')),
                ('description', models.TextField(null=True)),
                ('datefrom', models.DateField(null=True)),
                ('dateto', models.DateField(null=True)),
                ('pricefrom', models.SmallIntegerField(default=0)),
                ('priceto', models.SmallIntegerField(default=0)),
                ('location', models.CharField(max_length=4096, verbose_name='location')),
                ('status', models.SmallIntegerField(default=0)),
                ('detail', models.TextField(null=True, verbose_name='Detail')),
                ('thumbnail', models.CharField(max_length=2048, null=True, verbose_name='thumbnail')),
                ('type', models.SmallIntegerField(default=1)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ProductPic',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('url', models.CharField(max_length=4096)),
                ('name', models.CharField(default=b'', max_length=4096)),
                ('type', models.SmallIntegerField(default=0)),
                ('product', models.ForeignKey(to='product.AdaptorProduct')),
            ],
            options={
                'abstract': False,
                'db_table': 'pic',
            },
        ),
        migrations.AddField(
            model_name='adaptorattendcy',
            name='product',
            field=models.ForeignKey(to='product.AdaptorProduct'),
        ),
    ]
