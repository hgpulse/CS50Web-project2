# Generated by Django 3.1 on 2020-08-25 15:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0078_listing_watchlist'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bid',
            name='price',
            field=models.IntegerField(),
        ),
    ]
