# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('df_user', '0002_auto_20170802_1025'),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('create_time', models.DateTimeField(help_text=b'\xe5\x88\x9b\xe5\xbb\xba\xe6\x97\xb6\xe9\x97\xb4', auto_now_add=True)),
                ('update_time', models.DateTimeField(help_text=b'\xe6\x9b\xb4\xe6\x96\xb0\xe6\x97\xb6\xe9\x97\xb4', auto_now=True)),
                ('is_delete', models.BooleanField(default=False, help_text=b'\xe5\x88\xa0\xe9\x99\xa4\xe6\xa0\x87\xe8\xae\xb0')),
                ('recipicent_name', models.CharField(help_text=b'\xe6\x94\xb6\xe4\xbb\xb6\xe4\xba\xba', max_length=20)),
                ('recipicent_addr', models.CharField(help_text=b'\xe6\x94\xb6\xe4\xbb\xb6\xe5\x9c\xb0\xe5\x9d\x80', max_length=256)),
                ('recipicent_phone', models.CharField(help_text=b'\xe8\x81\x94\xe7\xb3\xbb\xe7\x94\xb5\xe8\xaf\x9d', max_length=11)),
                ('zip_code', models.CharField(help_text=b'\xe9\x82\xae\xe7\xbc\x96', max_length=6, null=True, blank=True)),
                ('is_default', models.BooleanField(default=False, help_text=b'\xe6\x98\xaf\xe5\x90\xa6\xe9\xbb\x98\xe8\xae\xa4')),
                ('passport', models.ForeignKey(help_text=b'\xe6\x89\x80\xe5\xb1\x9e\xe8\xb4\xa6\xe6\x88\xb7', to='df_user.Passport')),
            ],
            options={
                'db_table': 's_user_address',
            },
        ),
    ]
