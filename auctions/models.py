from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    listing = models.ManyToManyField("Listing", blank=True, related_name="users")

    def __str__(self):
        return f"{self.username}"

class Listing(models.Model):

    NO_CATEGORY = 'NO_CAT'
    FURNITURE = 'FUR'
    COMPUTER = 'COM'
    COMPUTER_ACCESSORIES = 'COM_AS'
    TOYS = 'TS'
    GARDEN_UTILITIES = 'GRD_UTIL'

    CATEGORIES = [
        (NO_CATEGORY, "No category"),
        (FURNITURE, "Furniture"),
        (COMPUTER, "Computer"),
        (COMPUTER_ACCESSORIES, "Computer Accessories"),
        (TOYS, "Toys"),
        (GARDEN_UTILITIES, "Garden Utilities"),
    ]

    title = models.CharField(max_length=64)
    description = models.TextField(max_length=1000)
    price = models.IntegerField()
    date_of_post = models.DateTimeField(auto_now_add=True)
    url_picture = models.CharField(max_length=500)
    category = models.CharField(max_length=100, choices=CATEGORIES, default=NO_CATEGORY)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings")

    def __str__(self):
        return f"Title: {self.title} - Price: {self.price} - Description: {self.description} - Date: {self.date_of_post} - Category: {self.category} - Posted by: {self.user_id}"

class Bid(models.Model):
    bid = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="listings", default=1)

    def __str__(self):
        return f"User: {self.user} made a bid of {self.bid} on {self.listing.title}"


class Comment(models.Model):
    comment = models.CharField(max_length=1000)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments", default=1)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="discussions", default=1)