# Generated by Django 3.2.5 on 2022-03-23 14:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shopowner', '0009_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='discount',
            field=models.FloatField(default='0'),
        ),
    ]