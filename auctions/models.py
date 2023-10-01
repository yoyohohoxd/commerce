from django.contrib.auth.models import AbstractUser
from django.db import models
import datetime


class User(AbstractUser):
    pass

class AuctionListings(models.Model):
    '''
    Class for all auction listings. Class containts: "title", "description", "price".

    '''
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=254)
    price = models.IntegerField()
    date_of_post = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Title: {self.title} - Price: {self.price} - Description: {self.description} - Date: {self.date_of_post}"

class Bids(models.Model):
    bid = models.IntegerField()


class Comments(models.Model):
    comment = models.CharField(max_length=1000)