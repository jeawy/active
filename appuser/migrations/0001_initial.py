# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='BaseUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(null=True, verbose_name='last login', blank=True)),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('modify_date', models.DateTimeField(auto_now=True)),
                ('username', models.CharField(default='\u672a\u586b\u5199', unique=True, max_length=50, verbose_name='\u59d3\u540d')),
                ('email', models.EmailField(unique=True, max_length=255, verbose_name='\u7535\u5b50\u90ae\u7bb1')),
                ('is_active', models.BooleanField(default=True, verbose_name='\u662f\u5426\u6709\u6548')),
                ('is_admin', models.BooleanField(default=False, verbose_name='\u662f\u5426\u4e3a\u7ba1\u7406\u5458')),
                ('is_head_portrait', models.BooleanField(default=False, verbose_name='\u662f\u5426\u4fdd\u5b58\u4e86\u4e0a\u4f20\u540e\u7684\u5934\u50cf')),
                ('head_portrait', models.ImageField(default=b'/media/portrait/no_img/no_portrait1.jpg', upload_to=b'portrait', verbose_name='\u9009\u62e9\u5934\u50cf')),
                ('email_verified', models.BooleanField(default=False, verbose_name='\u662f\u5426\u4fdd\u5b58\u4e86\u90ae\u7bb1')),
                ('social_user_status', models.IntegerField(default=0, verbose_name='\u7b2c\u4e09\u65b9\u7528\u6237\u72b6\u6001')),
                ('social_site_name', models.IntegerField(default=0, verbose_name='\u7b2c\u4e09\u65b9\u540d\u79f0')),
                ('social_user_id', models.CharField(default='\u672a\u586b\u5199', max_length=255, verbose_name='\u7b2c\u4e09\u65b9\u7528\u6237ID')),
                ('thumbnail_portait', models.ImageField(default=b'/media/portrait/no_img/no_portrait1.jpg', upload_to=b'portrait', verbose_name='\u5934\u50cf\u7f29\u7565\u56fe')),
                ('msg_mark', models.BooleanField(default=False, verbose_name='\u6709\u65b0\u6d88\u606f')),
            ],
            options={
                'permissions': (('admin_management', 'manage group, permission and user'),),
            },
        ),
        migrations.CreateModel(
            name='VerifyCode',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('email', models.EmailField(max_length=255)),
                ('code', models.CharField(default='', max_length=50, verbose_name='code')),
                ('type', models.CharField(default=b'0', max_length=5, verbose_name='type')),
            ],
        ),
        migrations.CreateModel(
            name='AdaptorUser',
            fields=[
                ('baseuser_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='appuser.BaseUser')),
                ('cart_num', models.IntegerField(default=0)),
            ],
            options={
                'db_table': 'user',
            },
            bases=('appuser.baseuser',),
        ),
        migrations.AddField(
            model_name='baseuser',
            name='groups',
            field=models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Group', blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', verbose_name='groups'),
        ),
        migrations.AddField(
            model_name='baseuser',
            name='user_permissions',
            field=models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Permission', blank=True, help_text='Specific permissions for this user.', verbose_name='user permissions'),
        ),
    ]
