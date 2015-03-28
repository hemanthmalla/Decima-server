# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rest_api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='asked_by',
            field=models.ForeignKey(related_name='asked', to='rest_api.User'),
            preserve_default=True,
        ),
    ]
