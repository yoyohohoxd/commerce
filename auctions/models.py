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
    date_of_post = models.DateTimeField(auto_now_add=True)
    url_picture = models.CharField(max_length=100)
    category = models.CharField(max_length=100, default='No Category')

    def __str__(self):
        return f"Title: {self.title} - Price: {self.price} - Description: {self.description} - Date: {self.date_of_post} - Category: {self.category}"

class Bids(models.Model):
    bid = models.IntegerField()


class Comments(models.Model):
    comment = models.CharField(max_length=1000)