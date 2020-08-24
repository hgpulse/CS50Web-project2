# Generated by Django 3.1 on 2020-08-24 14:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0072_auto_20200824_1445'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='watchlist',
            name='listing_list',
        ),
        migrations.AddField(
            model_name='listing',
            name='watchlist',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='auctions.watchlist'),
        ),
    ]