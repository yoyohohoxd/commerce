from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms

#Import class AuctionListings to use it I think
from .models import AuctionListings

from .models import User


class NewArticleForm(forms.Form):
    title = forms.CharField(label="", widget=forms.TextInput(attrs={'placeholder': 'Enter a title'}))
    description = forms.CharField(label="", widget=forms.Textarea)
    price = forms.IntegerField(label="", widget=forms.TextInput(attrs={'placeholder': 'Enter the starting bid'}))
    url_picture = forms.CharField(label="", required=False, widget=forms.TextInput(attrs={'placeholder': 'Optional URL for picture'}))
    

categories = ["", "Furniture", "Computer", "Computer Accessories", "Toys", "Garden Utilities"]

def index(request):
    return render(request, "auctions/index.html", {
        "auction_listings": AuctionListings.objects.all()
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


def create_listing(request):

    if request.method == "POST":
        new_article = NewArticleForm(request.POST)
        if new_article.is_valid():
            AuctionListings(title = new_article.cleaned_data["title"], 
                            description = new_article.cleaned_data["description"], 
                            price = new_article.cleaned_data["price"],
                            url_picture = new_article.cleaned_data["url_picture"],
                            category = request.POST["category"] #FIX THIS LATER BY ADDING CATEGORY TO THE FORM
                            ).save()
            

    return render(request, "auctions/create_listing.html", {
        "input_field": NewArticleForm(),
        "categories": categories
    })