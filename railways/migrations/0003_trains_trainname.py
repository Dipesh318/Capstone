# Generated by Django 2.1.7 on 2020-07-15 10:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('railways', '0002_city_days_passenger_trains'),
    ]

    operations = [
        migrations.AddField(
            model_name='trains',
            name='trainName',
            field=models.CharField(default='Express', max_length=20),
        ),
    ]
