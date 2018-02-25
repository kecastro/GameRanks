# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0007_auto_20180204_1721'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='cover',
            field=models.CharField(null=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='game',
            name='rating',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='game',
            name='release',
            field=models.CharField(null=True, max_length=20),
        ),
        migrations.AlterField(
            model_name='game',
            name='screenshots',
            field=models.CharField(null=True, max_length=600),
        ),
    ]
