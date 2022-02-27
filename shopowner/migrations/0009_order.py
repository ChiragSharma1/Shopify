# Generated by Django 3.2.5 on 2022-02-26 14:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0004_customer_image'),
        ('shopowner', '0008_remove_notification_product'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_price', models.IntegerField(default=0)),
                ('completed', models.BooleanField(default=False)),
                ('count', models.IntegerField(default=1)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='customer.customer')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shopowner.product')),
                ('shop', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shopowner.shop')),
            ],
        ),
    ]
