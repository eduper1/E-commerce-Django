from django.contrib.auth import REDIRECT_FIELD_NAME, authenticate, login, logout
from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from datetime import datetime
from . import forms

from .models import *


def index(request):
    listings = Auction_listings.objects.all()
    return render(request, "auctions/index.html", {
        "amounts": Bid.objects.all(),
        "listings": listings,
        "categories": Category.objects.all(),
    })
    
def list_page(request, list_id):
    if request.user.is_authenticated:
        list_auction = Auction_listings.objects.get(id=list_id)
        categories = Category.objects.filter(id = list_id)
        comment_text = forms.Create_comment()
        return render(request, "auctions/auc_details.html", {
            "detail": list_auction,
            "cats":categories,
            "user": request.user,
            "comments": list_auction.comment.all(),
            "com_form":comment_text,
        })
    else:
        list_auction = Auction_listings.objects.get(id =list_id)
        return render(request, "auctions/auc_details.html", {
            "detail":list_auction
        })
        # return render(request, "auctions/auc_details.html", {
        #     "detail": list_auction,
        # })

#@login_required(REDIRECT_FIELD_NAME= "login")
def create_listing(request):
    form = forms.Create_listing(request.POST,request.FILES)
    if request.user.is_authenticated:
        if request.method == "POST":
            form = form
            if form.is_valid():
                text = form.data["auc_created_by"]
                form.save()
            else:
                return render(request, "auctions/newListing.html",{
                    "form":form,
                })        
        return render (request,"auctions/newListing.html", {
            "form": forms.Create_listing()
        })
        
def comment(request,list_id):
    if request.user.is_authenticated:
        list_auction = Auction_listings.objects.get(pk=list_id)
        if request.method == 'POST':
            comment_text = forms.Create_comment(request.POST)
            if comment_text.is_valid():                                                                                                                                         
                com_t = comment_text.save(commit=False)
                # com_t.comment = comment_text["comment"]
                com_t.comment_on = list_auction
                com_t.comment_by = request.user
                com_t.save()
                # print(com_t)
            
                return HttpResponseRedirect(reverse("auctions_list", args=(list_auction.id,)))
            else:
                return render(request, "auctions/auc_details.html", {
                    "detail": list_auction,
                    # "cats":categories,
                    "user": request.user,
                    "comments": list_auction.comment.all(),
                    "com_form":comment_text,
                })
        return render (request,"auctions/auc_details.html", {
            "detail": list_auction,
            "user": request.user,
            "comments": list_auction.comment.all(),
            "com_form":comment_text()
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
