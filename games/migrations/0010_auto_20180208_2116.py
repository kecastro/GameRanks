# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0009_auto_20180205_1859'),
    ]

    operations = [
        migrations.AddField(
            model_name='exchange',
            name='creator_platform',
            field=models.CharField(choices=[('Xbox One', 'Xbox One'), ('Xbox 360', 'Xbox 360'), ('PlayStation 4', 'PlayStation 4'), ('PlayStation 3', 'PlayStation 3'), ('PlayStation Vita', 'PlayStation Vita'), ('Wii U', 'Wii U'), ('Nintendo 3DS', 'Nintendo 3DS')], max_length=30, default=('Xbox One', 'Xbox One')),
        ),
        migrations.AddField(
            model_name='exchange',
            name='guest_platform',
            field=models.CharField(choices=[('Xbox One', 'Xbox One'), ('Xbox 360', 'Xbox 360'), ('PlayStation 4', 'PlayStation 4'), ('PlayStation 3', 'PlayStation 3'), ('PlayStation Vita', 'PlayStation Vita'), ('Wii U', 'Wii U'), ('Nintendo 3DS', 'Nintendo 3DS')], max_length=30, default=('Xbox One', 'Xbox One')),
        ),
    ]
