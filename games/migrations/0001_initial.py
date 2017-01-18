# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Console',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=30)),
                ('votes', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Exchange',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('exchange_state', models.IntegerField(default=0)),
            ],
            options={
                'ordering': ['exchange_state'],
            },
        ),
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('year', models.CharField(max_length=10)),
                ('votes', models.IntegerField(default=0)),
                ('cover', models.CharField(max_length=250)),
                ('igdb_id', models.IntegerField()),
                ('console', models.ForeignKey(to='games.Console')),
            ],
        ),
        migrations.CreateModel(
            name='UserAccount',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('gamer_id', models.CharField(max_length=100, null=True)),
                ('picture', models.CharField(max_length=250, default='None')),
                ('games_owned', models.ManyToManyField(to='games.Game', related_name='games_owned', blank=True)),
                ('games_wanted', models.ManyToManyField(to='games.Game', related_name='games_wanted', blank=True)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Vote',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('game', models.ForeignKey(to='games.Game')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='exchange',
            name='creator',
            field=models.ForeignKey(related_name='exchange_creator', to='games.UserAccount'),
        ),
        migrations.AddField(
            model_name='exchange',
            name='game_creator',
            field=models.ForeignKey(related_name='exchange_game_creator', to='games.Game'),
        ),
        migrations.AddField(
            model_name='exchange',
            name='game_guest',
            field=models.ForeignKey(related_name='exchange_game_guest', to='games.Game'),
        ),
        migrations.AddField(
            model_name='exchange',
            name='guest',
            field=models.ForeignKey(related_name='exchange_guest', to='games.UserAccount'),
        ),
    ]
