# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ridevide_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='ride',
            name='luggage',
            field=models.PositiveIntegerField(default=1),
            preserve_default=False,
        ),
    ]
