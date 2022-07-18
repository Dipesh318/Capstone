# Generated by Django 2.1.7 on 2020-07-15 10:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('railways', '0005_passenger_trainno'),
    ]

    operations = [
        migrations.CreateModel(
            name='booking',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('AC_I', models.IntegerField(default=48)),
                ('AC_II', models.IntegerField(default=54)),
                ('AC_III', models.IntegerField(default=288)),
                ('Sleeper', models.IntegerField(default=576)),
                ('train', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='railways.trains')),
            ],
        ),
    ]
