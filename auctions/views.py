from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms

from .models import User

#Import class Listing to use it I think
from .models import User, Listing, Bid, Comment
from .forms import NewListingForm, CommentsForm


def index(request):

    return render(request, "auctions/index.html", {
        "auction_listings": Listing.objects.all()
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

            # Create, but don't save the new Listing --> NewListingForm instance
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

    # Gets id of currently visited listing
    listing = Listing.objects.get(id=listing_id)
    
    # Get current highest bid on listing
    highest_bid = Bid.objects.filter(listing=listing).order_by('bid').last()

    # Initialize CommentsForm
    formset = CommentsForm()

    # Gets all comments on this listing
    comments = Comment.objects.filter(listing=listing_id)
    print(comments)

    # Check name of button from HTML to make sure right instructions are given
    if request.method == "POST":

        # Get currently logged in user
        user = request.user
        user_id = user.id

        # Gets current user
        watcher = User.objects.get(id=user_id)
        #print(f"USER ({user.username}): {watcher.listing.all()}")

        # Goes through the AuctionListing objects with a filter that checks 'users' (related_name) in User class
        # If no match is found "watched" will be empty and will return False when called below with .exists()
        watched = Listing.objects.filter(users=user_id, id=listing_id).values()

        # If user clicks the add/remove watchlist
        if "watchlist" in request.POST:  
            if watched.exists():
                listing.users.remove(watcher)
            else:
                listing.users.add(watcher)

        # If user submits a bid
        elif "submit_bid" in request.POST:

            # Get current bid from page and convert to int
            current_bid = int(request.POST["bid"])

            # Bid made must be higher than or equal to the current price and currently highest bid
            if current_bid >= listing.price and current_bid > highest_bid.bid:
                Bid.objects.create(bid=current_bid, user=watcher, listing=listing)

                # Get new highest bid so that the website is updated by next return
                highest_bid = Bid.objects.filter(listing=listing).order_by('bid').last()
            else:
                offer_declined = True # Is there another way to check this?
                # Would be cool to turn this into a popup
                return render(request, "auctions/listing.html", {
                    "user": user,
                    "listing": listing,
                    "is_watching": watched.exists(),
                    "offer_declined": offer_declined,
                    "highest_bid": highest_bid.bid,
                    "formset": formset,
                    "comments": comments
                })
            
        # If user submits a comment
        elif "submit_comment" in request.POST:

            formset = CommentsForm(request.POST)

            if formset.is_valid():

                comment = formset.cleaned_data
                comment = comment.get('comment')
                Comment.objects.create(comment=comment, user=watcher, listing=listing)

            return render(request, "auctions/listing.html", {
                    "user": user,
                    "listing": listing,
                    "is_watching": watched.exists(),
                    "highest_bid": highest_bid.bid,
                    "formset": formset,
                    "comments": comments
            })
        

    #print(f"RIGHT NOW {listing.users.all()} FOLLOW(S) ({listing.title}): ")
    return render(request, "auctions/listing.html", {
        "listing": listing,
        "highest_bid": highest_bid.bid,
        "formset": formset,
        "comments": comments
    })

def watchlist(request):

    user = request.user

    instance = User.objects.get(id=user.id)

    # Get the listings title
    watchlist_for_user = instance.listing.all().values("id", "title")

    return render(request, "auctions/watchlist.html", {
        "user": user,
        "watchlist": watchlist_for_user
    })