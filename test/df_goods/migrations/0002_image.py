# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('df_goods', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('create_time', models.DateTimeField(help_text=b'\xe5\x88\x9b\xe5\xbb\xba\xe6\x97\xb6\xe9\x97\xb4', auto_now_add=True)),
                ('update_time', models.DateTimeField(help_text=b'\xe6\x9b\xb4\xe6\x96\xb0\xe6\x97\xb6\xe9\x97\xb4', auto_now=True)),
                ('is_delete', models.BooleanField(default=False, help_text=b'\xe5\x88\xa0\xe9\x99\xa4\xe6\xa0\x87\xe8\xae\xb0')),
                ('img_url', models.ImageField(help_text=b'\xe5\x9b\xbe\xe7\x89\x87\xe8\xb7\xaf\xe5\xbe\x84', upload_to=b'goods')),
                ('is_def', models.BooleanField(default=False, help_text=b'\xe6\x98\xaf\xe5\x90\xa6\xe9\xbb\x98\xe8\xae\xa4')),
                ('goods', models.ForeignKey(help_text=b'\xe6\x89\x80\xe5\xb1\x9e\xe5\x95\x86\xe5\x93\x81', to='df_goods.Goods')),
            ],
            options={
                'db_table': 's_goods_image',
            },
        ),
    ]
