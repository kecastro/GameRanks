# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0006_auto_20180204_1657'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='release',
            field=models.CharField(max_length=20),
        ),
    ]
