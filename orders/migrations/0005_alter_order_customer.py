# Generated by Django 4.1.13 on 2024-01-10 05:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0004_alter_order_customer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='customer',
            field=models.PositiveIntegerField(),
        ),
    ]
