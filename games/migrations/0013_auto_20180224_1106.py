# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0012_auto_20180224_1105'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='release',
            field=models.DateField(null=True),
        ),
    ]
