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
            name='Exchange',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('creator_platform', models.CharField(max_length=30, choices=[('Xbox One', 'Xbox One'), ('Xbox 360', 'Xbox 360'), ('PlayStation 4', 'PlayStation 4'), ('PlayStation 3', 'PlayStation 3'), ('PlayStation Vita', 'PlayStation Vita'), ('Wii U', 'Wii U'), ('Nintendo 3DS', 'Nintendo 3DS')])),
                ('guest_platform', models.CharField(max_length=30, choices=[('Xbox One', 'Xbox One'), ('Xbox 360', 'Xbox 360'), ('PlayStation 4', 'PlayStation 4'), ('PlayStation 3', 'PlayStation 3'), ('PlayStation Vita', 'PlayStation Vita'), ('Wii U', 'Wii U'), ('Nintendo 3DS', 'Nintendo 3DS')])),
                ('exchange_state', models.IntegerField(default=0)),
                ('accepted', models.BooleanField(default=False)),
            ],
            options={
                'ordering': ['exchange_state'],
            },
        ),
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('igdb', models.CharField(max_length=10)),
                ('name', models.CharField(max_length=50)),
                ('rating', models.FloatField(null=True)),
                ('release', models.DateField(null=True)),
                ('screenshots', models.CharField(null=True, max_length=600)),
                ('cover', models.CharField(null=True, max_length=100)),
                ('platform', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='TradeOption',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('type', models.BooleanField()),
                ('platform', models.CharField(max_length=30, choices=[('Xbox One', 'Xbox One'), ('Xbox 360', 'Xbox 360'), ('PlayStation 4', 'PlayStation 4'), ('PlayStation 3', 'PlayStation 3'), ('PlayStation Vita', 'PlayStation Vita'), ('Wii U', 'Wii U'), ('Nintendo 3DS', 'Nintendo 3DS')])),
                ('game', models.ForeignKey(to='games.Game', related_name='tradable_game')),
            ],
        ),
        migrations.CreateModel(
            name='UserAccount',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('gamer_id', models.CharField(null=True, max_length=100)),
                ('picture', models.CharField(max_length=250, default='None')),
                ('phone', models.CharField(max_length=15, default='(000)000-0000')),
                ('city', models.CharField(max_length=30, default='Colombia')),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='tradeoption',
            name='user',
            field=models.ForeignKey(to='games.UserAccount', related_name='trading_user'),
        ),
        migrations.AddField(
            model_name='exchange',
            name='creator',
            field=models.ForeignKey(to='games.UserAccount', related_name='exchange_creator'),
        ),
        migrations.AddField(
            model_name='exchange',
            name='game_creator',
            field=models.ForeignKey(to='games.Game', related_name='exchange_game_creator'),
        ),
        migrations.AddField(
            model_name='exchange',
            name='game_guest',
            field=models.ForeignKey(to='games.Game', related_name='exchange_game_guest'),
        ),
        migrations.AddField(
            model_name='exchange',
            name='guest',
            field=models.ForeignKey(to='games.UserAccount', related_name='exchange_guest'),
        ),
    ]
