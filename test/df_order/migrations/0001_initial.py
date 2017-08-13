# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('df_goods', '0003_browsehistory'),
        ('df_user', '0003_address'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderBasic',
            fields=[
                ('create_time', models.DateTimeField(help_text=b'\xe5\x88\x9b\xe5\xbb\xba\xe6\x97\xb6\xe9\x97\xb4', auto_now_add=True)),
                ('update_time', models.DateTimeField(help_text=b'\xe6\x9b\xb4\xe6\x96\xb0\xe6\x97\xb6\xe9\x97\xb4', auto_now=True)),
                ('is_delete', models.BooleanField(default=False, help_text=b'\xe5\x88\xa0\xe9\x99\xa4\xe6\xa0\x87\xe8\xae\xb0')),
                ('order_id', models.CharField(help_text=b'\xe8\xae\xa2\xe5\x8d\x95id', max_length=64, serialize=False, primary_key=True)),
                ('total_count', models.IntegerField(default=1, help_text=b'\xe5\x95\x86\xe5\x93\x81\xe6\x80\xbb\xe6\x95\xb0')),
                ('total_price', models.DecimalField(help_text=b'\xe5\x95\x86\xe5\x93\x81\xe6\x80\xbb\xe9\xa2\x9d', max_digits=10, decimal_places=2)),
                ('transit_price', models.DecimalField(help_text=b'\xe8\xae\xa2\xe5\x8d\x95\xe8\xbf\x90\xe8\xb4\xb9', max_digits=10, decimal_places=2)),
                ('pay_method', models.IntegerField(default=1, help_text=b'\xe6\x94\xaf\xe4\xbb\x98\xe6\x96\xb9\xe5\xbc\x8f')),
                ('order_status', models.IntegerField(default=1, help_text=b'\xe8\xae\xa2\xe5\x8d\x95\xe7\x8a\xb6\xe6\x80\x81')),
                ('addr', models.ForeignKey(help_text=b'\xe6\x94\xb6\xe4\xbb\xb6\xe5\x9c\xb0\xe5\x9d\x80', to='df_user.Address')),
                ('passport', models.ForeignKey(help_text=b'\xe7\x94\xa8\xe6\x88\xb7', to='df_user.Passport')),
            ],
            options={
                'db_table': 's_order_basic',
            },
        ),
        migrations.CreateModel(
            name='OrderDetail',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('create_time', models.DateTimeField(help_text=b'\xe5\x88\x9b\xe5\xbb\xba\xe6\x97\xb6\xe9\x97\xb4', auto_now_add=True)),
                ('update_time', models.DateTimeField(help_text=b'\xe6\x9b\xb4\xe6\x96\xb0\xe6\x97\xb6\xe9\x97\xb4', auto_now=True)),
                ('is_delete', models.BooleanField(default=False, help_text=b'\xe5\x88\xa0\xe9\x99\xa4\xe6\xa0\x87\xe8\xae\xb0')),
                ('goods_count', models.IntegerField(default=1, help_text=b'\xe5\x95\x86\xe5\x93\x81\xe6\x95\xb0\xe7\x9b\xae')),
                ('goods_price', models.DecimalField(help_text=b'\xe5\x95\x86\xe5\x93\x81\xe4\xbb\xb7\xe6\xa0\xbc', max_digits=10, decimal_places=2)),
                ('goods', models.ForeignKey(help_text=b'\xe5\x95\x86\xe5\x93\x81', to='df_goods.Goods')),
                ('order', models.ForeignKey(help_text=b'\xe5\x9f\xba\xe6\x9c\xac\xe8\xae\xa2\xe5\x8d\x95', to='df_order.OrderBasic')),
            ],
            options={
                'db_table': 's_order_detail',
            },
        ),
    ]
