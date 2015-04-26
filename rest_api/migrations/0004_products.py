# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rest_api', '0003_auto_20150405_2100'),
    ]

    operations = [
        migrations.CreateModel(
            name='Products',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('identifier', models.IntegerField()),
                ('title', models.CharField(max_length=100)),
                ('source', models.CharField(default=b'', max_length=256)),
                ('image', models.CharField(max_length=256)),
                ('final_price', models.IntegerField(default=0)),
                ('item_price', models.IntegerField(default=0)),
                ('discount_percent', models.IntegerField(default=0)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
