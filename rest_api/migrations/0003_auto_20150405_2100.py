# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rest_api', '0002_auto_20150326_2330'),
    ]

    operations = [
        migrations.CreateModel(
            name='DecimaQuestions',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('key', models.CharField(max_length=50, blank=True)),
                ('status', models.BooleanField(default=True)),
                ('question', models.ForeignKey(to='rest_api.Question')),
                ('user', models.ForeignKey(to='rest_api.User')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='question',
            name='date_time_asked',
            field=models.DateTimeField(auto_now_add=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='user',
            name='phone',
            field=models.CharField(max_length=13),
            preserve_default=True,
        ),
    ]
