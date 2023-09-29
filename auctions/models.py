from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class AuctionListings(models.Model):
    '''
    First have the title, description, price, and a date of post.

    '''
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=254)
    price = models.IntegerField()

    def __str__(self):
        return f"Title: {self.title} - Price: {self.price} - Description: {self.description}"

class Bids(models.Model):
    bid = models.IntegerField()


class Comments(models.Model):
    comment = models.CharField(max_length=1000)