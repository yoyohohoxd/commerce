from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms

from .models import User

#Import class AuctionListings to use it I think
from .models import User
from .models import AuctionListings
from .forms import NewListingForm


def index(request):

    print(AuctionListings.objects.all())

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

# Requires login - if not then get redirected to login page
@login_required(login_url='/login')
def create_listing(request):
    if request.method == "POST":
        
        # Create a form instance with POST data
        formset = NewListingForm(request.POST)
        if formset.is_valid():

            # Create, but don't save the new AuctionListing --> NewListingForm instance
            instance = formset.save(commit=False)

            # Assign this instance of the formset with the user id, since it isn't declared in the form 
            instance.user = request.user

            # Actually save the instance
            instance.save()
        return HttpResponseRedirect(reverse("index"))
    else:
        formset = NewListingForm()
        return render(request, "auctions/create_listing.html", {
            "formset": formset
        })
    

def listing(request, listing_id):

    if request.method == "POST":
        user = request.user
        
    
    listing = AuctionListings.objects.get(id=listing_id)
    return render(request, "auctions/listing.html", {
        "user": user,
        "listing": listing
    })

def watchlist(request, user):

    user = User.objects.get(username=user)

    return render(request, "auctions/watchlist.html", {
        "user": user
    })