# Generated by Django 3.1 on 2020-08-24 08:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0050_auto_20200824_0834'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='watchlist',
            name='user',
        ),
    ]
