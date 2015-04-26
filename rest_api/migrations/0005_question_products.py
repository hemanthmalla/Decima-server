# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rest_api', '0004_products'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='products',
            field=models.ManyToManyField(to='rest_api.Products', null=True, blank=True),
            preserve_default=True,
        ),
    ]
