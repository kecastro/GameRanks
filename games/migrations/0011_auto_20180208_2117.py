# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0010_auto_20180208_2116'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exchange',
            name='creator_platform',
            field=models.CharField(choices=[('Xbox One', 'Xbox One'), ('Xbox 360', 'Xbox 360'), ('PlayStation 4', 'PlayStation 4'), ('PlayStation 3', 'PlayStation 3'), ('PlayStation Vita', 'PlayStation Vita'), ('Wii U', 'Wii U'), ('Nintendo 3DS', 'Nintendo 3DS')], max_length=30),
        ),
        migrations.AlterField(
            model_name='exchange',
            name='guest_platform',
            field=models.CharField(choices=[('Xbox One', 'Xbox One'), ('Xbox 360', 'Xbox 360'), ('PlayStation 4', 'PlayStation 4'), ('PlayStation 3', 'PlayStation 3'), ('PlayStation Vita', 'PlayStation Vita'), ('Wii U', 'Wii U'), ('Nintendo 3DS', 'Nintendo 3DS')], max_length=30),
        ),
    ]
