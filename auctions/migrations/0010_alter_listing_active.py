# Generated by Django 4.2.4 on 2023-10-18 20:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0009_listing_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='active',
            field=models.BooleanField(default=True),
        ),
    ]