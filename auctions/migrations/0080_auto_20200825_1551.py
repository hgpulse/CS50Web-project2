# Generated by Django 3.1 on 2020-08-25 15:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0079_auto_20200825_1532'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bid',
            name='user',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='comment',
            name='user',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
