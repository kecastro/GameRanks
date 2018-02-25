# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0004_auto_20170121_2120'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vote',
            name='game',
        ),
        migrations.RemoveField(
            model_name='vote',
            name='user',
        ),
        migrations.RemoveField(
            model_name='game',
            name='console',
        ),
        migrations.RemoveField(
            model_name='game',
            name='igdb_id',
        ),
        migrations.RemoveField(
            model_name='game',
            name='votes',
        ),
        migrations.RemoveField(
            model_name='game',
            name='year',
        ),
        migrations.AddField(
            model_name='game',
            name='igdb',
            field=models.CharField(max_length=10, default=0),
        ),
        migrations.AddField(
            model_name='game',
            name='platform',
            field=models.CharField(max_length=100, default='Undefined'),
        ),
        migrations.AddField(
            model_name='game',
            name='rating',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='game',
            name='release',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='game',
            name='screenshots',
            field=models.CharField(max_length=600, default='Undefined'),
        ),
        migrations.AlterField(
            model_name='game',
            name='cover',
            field=models.CharField(max_length=100, default='Undefined'),
        ),
        migrations.AlterField(
            model_name='game',
            name='name',
            field=models.CharField(max_length=50, default='Undefined'),
        ),
        migrations.DeleteModel(
            name='Console',
        ),
        migrations.DeleteModel(
            name='Vote',
        ),
    ]
