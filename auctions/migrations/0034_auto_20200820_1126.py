# Generated by Django 3.1 on 2020-08-20 11:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0033_remove_listing_owner'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bid',
            name='owner',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='owner',
        ),
        migrations.RemoveField(
            model_name='watch',
            name='owner',
        ),
    ]
