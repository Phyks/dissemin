# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-07-03 11:40


from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('papers', '0034_merge'),
    ]

    operations = [
        migrations.AlterField(
            model_name='oairecord',
            name='doi',
            field=models.CharField(blank=True, db_index=True, max_length=1024, null=True),
        ),
    ]
