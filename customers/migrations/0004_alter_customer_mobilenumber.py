# Generated by Django 4.1.13 on 2024-01-03 20:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0003_alter_customer_mobilenumber_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='mobileNumber',
            field=models.CharField(default='', max_length=12),
        ),
    ]