# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rest_api', '0006_auto_20150425_1814'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='peers_involved',
            field=models.ManyToManyField(to='rest_api.User', null=True, blank=True),
            preserve_default=True,
        ),
    ]
