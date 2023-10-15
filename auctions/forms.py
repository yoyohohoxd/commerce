from django.forms import ModelForm
from django import forms
from .models import Listing, Comment

class NewListingForm(ModelForm):

    # Overwrite the "url_picture" from the model to apply "required"-parameter
    url_picture = forms.CharField(required=False)

    class Meta:
        model = Listing
        fields = ['title', 'description', 'price', 'url_picture', 'category']

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'price': forms.TextInput(attrs={'class': 'form-control'}),
            'url_picture': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'})
        }


class CommentsForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment']

        widgets = {
            'comment': forms.Textarea(attrs={'class': 'form-control'}),
        }