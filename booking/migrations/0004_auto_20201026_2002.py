# Generated by Django 3.1.2 on 2020-10-26 11:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0003_auto_20201026_2000'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='terms_information_collection',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='booking',
            name='terms_information_refund',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='booking',
            name='terms_information_third_party',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='booking',
            name='terms_marketing',
            field=models.BooleanField(default=True),
        ),
    ]
