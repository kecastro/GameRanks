# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0005_auto_20180204_1652'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='cover',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='game',
            name='igdb',
            field=models.CharField(max_length=10),
        ),
        migrations.AlterField(
            model_name='game',
            name='name',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='game',
            name='platform',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='game',
            name='rating',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='game',
            name='release',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='game',
            name='screenshots',
            field=models.CharField(max_length=600),
        ),
    ]
