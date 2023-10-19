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

    # Get currently logged in user
    user = request.user
    user_id = user.id

    # Gets id of currently visited listing
    listing = Listing.objects.get(id=listing_id)
    
    # Get current highest bid on listing. Returns None if no bid has been made
    highest_bid = Bid.objects.filter(listing=listing).order_by('bid').last()

    # Initialize CommentsForm
    formset = CommentsForm()

    # Gets all comments on this listing
    comments = Comment.objects.filter(listing=listing_id)

    # Goes through the Listing objects with a filter that checks 'users' (related_name) in User class
    # If no match is found "on_watchlist" will be empty and will return False when called below with .exists()
    on_watchlist = Listing.objects.filter(users=user_id, id=listing_id).values()

    # Check name of button from HTML to make sure right instructions are given
    if request.method == "POST":
        
        # A better way to check if offer is declined?
        offer_declined = False

        # Gets current user
        current_user = User.objects.get(id=user_id)
        #print(f"USER ({user.username}): {current_user.listing.all()}")

        # If user in any way interacts with the website
        if "watchlist" in request.POST:
            if on_watchlist.exists():
                listing.users.remove(current_user)
            else:
                listing.users.add(current_user)

        # If user submits a bid
        elif "submit_bid" in request.POST:

            # Get current bid from page and convert to int
            current_bid = int(request.POST["bid"])

            # Bid made must be higher than or equal to the current price and currently highest bid
            if current_bid >= listing.price and current_bid > highest_bid.bid:
                Bid.objects.create(bid=current_bid, user=current_user, listing=listing)

                # Update highest bid so that the website is updated by next return
                highest_bid = Bid.objects.filter(listing=listing).order_by('bid').last()
            else:
                offer_declined = True # Is there another way to check this?
                # Would be cool to turn this into a popup

        # If user submits a comment
        elif "submit_comment" in request.POST:
            formset = CommentsForm(request.POST)
            if formset.is_valid():
                comment = formset.cleaned_data
                comment = comment.get('comment')
                Comment.objects.create(comment=comment, user=current_user, listing=listing)

        # If user closes bid, highest bid wins
        elif "close_listing" in request.POST:
            instance = listing
            instance.active = False
            instance.save()

        
        return render(request, "auctions/listing.html", {
            "user_id": user_id,
            "listing": listing,
            "is_watching": on_watchlist.exists(),
            "offer_declined": offer_declined,
            "highest_bid": highest_bid,
            "formset": formset,
            "comments": comments
        })
        
    else:
        #print(f"RIGHT NOW {listing.users.all()} FOLLOW(S) ({listing.title}): ")
        return render(request, "auctions/listing.html", {
            "user_id": user_id,
            "listing": listing,
            "is_watching": on_watchlist.exists(),
            "highest_bid": highest_bid,
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

def categories(request):
    categories = Listing.Categories.choices
    return render(request, "auctions/categories.html", {
        "categories": categories
    })

def category(request, category):

    l1 = Listing.objects.filter(category=category).order_by('title')

    return render(request, "auctions/category.html", {
        "listings": l1
    })