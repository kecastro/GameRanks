# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0008_auto_20180204_1734'),
    ]

    operations = [
        migrations.CreateModel(
            name='TradeOption',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('type', models.BooleanField()),
                ('platform', models.CharField(max_length=30, choices=[('Xbox One', 'Xbox One'), ('Xbox 360', 'Xbox 360'), ('PlayStation 4', 'PlayStation 4'), ('PlayStation 3', 'PlayStation 3'), ('PlayStation Vita', 'PlayStation Vita'), ('Wii U', 'Wii U'), ('Nintendo 3DS', 'Nintendo 3DS')])),
                ('game', models.ForeignKey(related_name='tradable_game', to='games.Game')),
            ],
        ),
        migrations.RemoveField(
            model_name='useraccount',
            name='games_owned',
        ),
        migrations.RemoveField(
            model_name='useraccount',
            name='games_wanted',
        ),
        migrations.AddField(
            model_name='tradeoption',
            name='user',
            field=models.ForeignKey(related_name='trading_user', to='games.UserAccount'),
        ),
    ]
