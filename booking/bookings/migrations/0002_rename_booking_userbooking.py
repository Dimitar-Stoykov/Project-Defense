# Generated by Django 4.2.11 on 2024-04-15 17:42

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rooms', '0002_delete_booking'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('bookings', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Booking',
            new_name='UserBooking',
        ),
    ]
