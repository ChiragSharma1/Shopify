# Generated by Django 3.2.5 on 2021-12-24 05:59

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shopowner', '0003_auto_20211224_1100'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shopowner',
            name='address',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='shopowner',
            name='age',
            field=models.IntegerField(null=True, validators=[django.core.validators.MinValueValidator(18)]),
        ),
        migrations.AlterField(
            model_name='shopowner',
            name='city',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='shopowner',
            name='state',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
