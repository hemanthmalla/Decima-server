# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rest_api', '0005_question_products'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='answers_by',
            field=models.ManyToManyField(related_name='answered', null=True, through='rest_api.Vote', to='rest_api.User', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='question',
            name='asked_by',
            field=models.ForeignKey(related_name='asked', blank=True, to='rest_api.User', null=True),
            preserve_default=True,
        ),
    ]
