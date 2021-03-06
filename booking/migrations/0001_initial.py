# Generated by Django 3.1.2 on 2020-10-21 08:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('hotel', '0002_auto_20201021_1711'),
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_from', models.DateField()),
                ('date_to', models.DateField()),
                ('phone_number', models.CharField(max_length=40)),
                ('adult', models.IntegerField()),
                ('child', models.IntegerField(default=0)),
                ('infant', models.IntegerField(default=0)),
                ('demand', models.TextField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=18)),
                ('discount', models.DecimalField(decimal_places=2, max_digits=18)),
                ('total', models.DecimalField(decimal_places=2, max_digits=18)),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hotel.room')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.user')),
            ],
            options={
                'db_table': 'bookings',
            },
        ),
        migrations.CreateModel(
            name='BookedRoom',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('booking', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='booking.booking')),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hotel.room')),
            ],
            options={
                'db_table': 'booked_rooms',
            },
        ),
    ]
