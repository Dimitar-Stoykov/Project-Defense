# Generated by Django 4.2.11 on 2024-04-17 21:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotels', '0009_alter_hotel_location'),
    ]

    operations = [
        migrations.AddField(
            model_name='hotel',
            name='cancel_period',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]
