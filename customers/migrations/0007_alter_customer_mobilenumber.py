# Generated by Django 4.1.13 on 2024-01-06 20:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0006_alter_customer_mobilenumber'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='mobileNumber',
            field=models.CharField(default=None, max_length=12, null=True),
        ),
    ]
