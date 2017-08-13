# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('df_user', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='passport',
            name='isDelete',
        ),
        migrations.AddField(
            model_name='passport',
            name='is_delete',
            field=models.BooleanField(default=False, help_text=b'\xe5\x88\xa0\xe9\x99\xa4\xe6\xa0\x87\xe8\xae\xb0'),
        ),
    ]
