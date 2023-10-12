# Generated by Django 4.2.4 on 2023-10-12 19:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_user_listing'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Bids',
            new_name='Bid',
        ),
        migrations.RenameModel(
            old_name='Comments',
            new_name='Comment',
        ),
        migrations.RenameModel(
            old_name='AuctionListings',
            new_name='Listing',
        ),
        migrations.AddField(
            model_name='user',
            name='bid',
            field=models.ManyToManyField(blank=True, related_name='bids', to='auctions.bid'),
        ),
    ]
