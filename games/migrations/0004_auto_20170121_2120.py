# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0003_auto_20170115_1336'),
    ]

    operations = [
        migrations.AddField(
            model_name='exchange',
            name='accepted',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='useraccount',
            name='city',
            field=models.CharField(default='Colombia', max_length=30),
        ),
        migrations.AddField(
            model_name='useraccount',
            name='phone',
            field=models.CharField(default='(000)000-0000', max_length=15),
        ),
    ]
