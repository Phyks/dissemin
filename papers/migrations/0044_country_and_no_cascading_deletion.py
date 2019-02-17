# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-29 19:11


from django.db import migrations, models
import django.db.models.deletion
import django_countries.fields


class Migration(migrations.Migration):

    dependencies = [
        ('papers', '0043_institutions_multiple_identifiers'),
    ]

    operations = [
        migrations.AlterField(
            model_name='institution',
            name='country',
            field=django_countries.fields.CountryField(blank=True, max_length=2, null=True),
        ),
        migrations.AlterField(
            model_name='researcher',
            name='department',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='papers.Department'),
        ),
        migrations.AlterField(
            model_name='researcher',
            name='institution',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='papers.Institution'),
        ),
    ]
