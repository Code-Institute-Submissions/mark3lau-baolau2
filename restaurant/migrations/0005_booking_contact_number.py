# Generated by Django 3.2.17 on 2023-02-21 22:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0004_booking_number_of_people'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='contact_number',
            field=models.CharField(default=0, max_length=20),
            preserve_default=False,
        ),
    ]
