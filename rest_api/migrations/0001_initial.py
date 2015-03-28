# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Option',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=128)),
                ('quest_id', models.IntegerField()),
                ('votes', models.IntegerField(default=0)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('statement', models.CharField(max_length=200)),
                ('is_active', models.BooleanField(default=True)),
                ('date_time_asked', models.DateTimeField()),
                ('date_time_answered', models.DateTimeField(null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('full_name', models.CharField(max_length=128)),
                ('email', models.EmailField(max_length=75)),
                ('phone', models.CharField(max_length=10)),
                ('gcm_id', models.CharField(max_length=200)),
                ('fb_id', models.CharField(max_length=100)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Vote',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('voted', models.BooleanField(default=False)),
                ('option', models.ForeignKey(to='rest_api.Option', null=True)),
                ('question', models.ForeignKey(to='rest_api.Question')),
                ('user_id', models.ForeignKey(to='rest_api.User')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='question',
            name='answers_by',
            field=models.ManyToManyField(related_name='answered', through='rest_api.Vote', to='rest_api.User'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='question',
            name='asked_by',
            field=models.OneToOneField(related_name='asked', to='rest_api.User'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='question',
            name='options',
            field=models.ManyToManyField(to='rest_api.Option'),
            preserve_default=True,
        ),
    ]
