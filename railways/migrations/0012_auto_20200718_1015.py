# Generated by Django 2.1.7 on 2020-07-18 10:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('railways', '0011_passenger_seat'),
    ]

    operations = [
        migrations.RenameField(
            model_name='passenger',
            old_name='train',
            new_name='train_info',
        ),
    ]