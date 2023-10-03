from django.forms import ModelForm
from django import forms
from .models import AuctionListings

class NewListingForm(ModelForm):

    url_picture = forms.CharField(required=False)

    class Meta:
        model = AuctionListings
        fields = ['title', 'description', 'price', 'url_picture', 'category']