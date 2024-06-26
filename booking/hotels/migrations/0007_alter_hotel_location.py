# Generated by Django 4.2.11 on 2024-04-15 19:32

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotels', '0006_alter_hotel_created_by'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hotel',
            name='location',
            field=models.CharField(error_messages='The location must be at least 10 characters long', max_length=100, validators=[django.core.validators.MinLengthValidator(10)]),
        ),
    ]
