# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Goods',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('create_time', models.DateTimeField(help_text=b'\xe5\x88\x9b\xe5\xbb\xba\xe6\x97\xb6\xe9\x97\xb4', auto_now_add=True)),
                ('update_time', models.DateTimeField(help_text=b'\xe6\x9b\xb4\xe6\x96\xb0\xe6\x97\xb6\xe9\x97\xb4', auto_now=True)),
                ('is_delete', models.BooleanField(default=False, help_text=b'\xe5\x88\xa0\xe9\x99\xa4\xe6\xa0\x87\xe8\xae\xb0')),
                ('goods_type_id', models.SmallIntegerField(help_text=b'\xe5\x95\x86\xe5\x93\x81\xe7\xa7\x8d\xe7\xb1\xbb', choices=[(1, b'\xe6\x96\xb0\xe9\xb2\x9c\xe6\xb0\xb4\xe6\x9e\x9c'), (2, b'\xe6\xb5\xb7\xe9\xb2\x9c\xe6\xb0\xb4\xe4\xba\xa7'), (3, b'\xe7\x8c\xaa\xe7\x89\x9b\xe7\xbe\x8a\xe8\x82\x89'), (4, b'\xe7\xa6\xbd\xe7\xb1\xbb\xe8\x9b\x8b\xe5\x93\x81'), (5, b'\xe6\x96\xb0\xe9\xb2\x9c\xe8\x94\xac\xe8\x8f\x9c'), (6, b'\xe9\x80\x9f\xe5\x86\xbb\xe9\xa3\x9f\xe5\x93\x81')])),
                ('goods_name', models.CharField(help_text=b'\xe5\x95\x86\xe5\x93\x81\xe5\x90\x8d\xe7\xa7\xb0', max_length=32)),
                ('goods_sub_title', models.CharField(help_text=b'\xe5\x95\x86\xe5\x93\x81\xe5\x89\xaf\xe6\xa0\x87\xe9\xa2\x98', max_length=128)),
                ('goods_price', models.DecimalField(help_text=b'\xe5\x95\x86\xe5\x93\x81\xe4\xbb\xb7\xe6\xa0\xbc', max_digits=10, decimal_places=2)),
                ('goods_ex_price', models.DecimalField(help_text=b'\xe5\x95\x86\xe5\x93\x81\xe8\xbf\x90\xe8\xb4\xb9', max_digits=10, decimal_places=2)),
                ('goods_unite', models.CharField(default=b'500g', help_text=b'\xe5\x95\x86\xe5\x93\x81\xe5\x8d\x95\xe4\xbd\x8d', max_length=16)),
                ('goods_info', tinymce.models.HTMLField(help_text=b'\xe5\x95\x86\xe5\x93\x81\xe6\x8f\x8f\xe8\xbf\xb0')),
                ('goods_stock', models.IntegerField(default=1, help_text=b'\xe5\x95\x86\xe5\x93\x81\xe5\xba\x93\xe5\xad\x98')),
                ('goods_status', models.SmallIntegerField(default=0, help_text=b'\xe5\x95\x86\xe5\x93\x81\xe7\x8a\xb6\xe6\x80\x81')),
                ('goods_sales', models.IntegerField(default=0, help_text=b'\xe5\x95\x86\xe5\x93\x81\xe9\x94\x80\xe9\x87\x8f')),
            ],
            options={
                'db_table': 's_goods',
            },
        ),
    ]
