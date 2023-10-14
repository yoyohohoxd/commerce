from django.forms import ModelForm
from django import forms
from .models import Listing

class NewListingForm(ModelForm):

    # Overwrite the "url_picture" from the model to apply "required"-parameter
    url_picture = forms.CharField(required=False)

    class Meta:
        model = Listing
        fields = ['title', 'description', 'price', 'url_picture', 'category']