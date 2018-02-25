# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0011_auto_20180208_2117'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='release',
            field=models.DateTimeField(null=True),
        ),
    ]
