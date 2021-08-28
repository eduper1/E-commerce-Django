from django.contrib.auth import REDIRECT_FIELD_NAME, authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from . import forms

from .models import *


def index(request):
    listings = Auction_listings.objects.all()
    return render(request, "auctions/index.html", {
        "amounts": Bid.objects.all(),
        "listings": listings
    })
    
def list_page(request, list_id):
    if request.user.is_authenticated:
        list_auction = Auction_listings.objects.get(pk=list_id)
        #comment_form = forms.Create_comment()
        categories = Category.objects.get(pk = list_id)
        #categories.auctions.add(list_auction)
        return render(request, "auctions/auc_details.html", {
            "detail": list_auction,
            "cats":categories,
            "user": request.user,
            #"form": comment_form
            #"": list_auction..all(),
            #"non_passenger": Passenger.objects.exclude(flights=flight).all()
        })
    else:
        list_auction = Auction_listings.objects.get(pk=list_id)
        return render(request, "auctions/auc_details.html", {
            "detail": list_auction,
            #"form": comment_form()
            #"": list_auction..all(),
            #"non_passenger": Passenger.objects.exclude(flights=flight).all()
        })

#@login_required(REDIRECT_FIELD_NAME= "login")
def create_listing(request):
    form = forms.Create_listing(request.POST,request.FILES)
    if request.user.is_authenticated:
        if request.method == "POST":
            form = form
            if form.is_valid():
                text = form.data["auc_created_by"]
                text = request.user
                form.save()
                #listing = Auction_listings.objects(form)
                #listing.save()
            else:
                return render(request, "auctions/newListing.html",{
                    "form":form,
                })        
        return render (request,"auctions/newListing.html", {
            "form": forms.Create_listing()
        })
        
"""
def comment(request):
    if request.user.is_authenticated:
        comment_form = forms.Create_comment()
        return render (request, "auctions/auc_details.html",{
            "form": comment_form
        })

"""        


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
