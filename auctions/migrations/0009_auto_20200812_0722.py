# Generated by Django 3.1 on 2020-08-12 07:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0008_auto_20200812_0622'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='image',
            field=models.ImageField(blank=True, default='images/jump_kitefoil.png', null=True, upload_to='images'),
        ),
    ]
