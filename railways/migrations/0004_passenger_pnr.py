# Generated by Django 2.1.7 on 2020-07-15 10:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('railways', '0003_trains_trainname'),
    ]

    operations = [
        migrations.AddField(
            model_name='passenger',
            name='PNR',
            field=models.CharField(default='XXX-XXXXXXX', max_length=11),
        ),
    ]
