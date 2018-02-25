# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0002_auto_20180225_1152'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='cover',
            field=models.CharField(null=True, max_length=1000),
        ),
        migrations.AlterField(
            model_name='game',
            name='name',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='game',
            name='platform',
            field=models.CharField(max_length=500),
        ),
    ]
