# Generated by Django 3.1 on 2020-08-20 11:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0036_auto_20200820_1142'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bid',
            name='date',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='comment',
            name='date',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='listing',
            name='date',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
