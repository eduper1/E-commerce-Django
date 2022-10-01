from django.contrib.auth import REDIRECT_FIELD_NAME, authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from datetime import datetime
from . import forms

from .models import *


def index(request):
    listings = Auction_listings.objects.all().order_by('-auc_date_published')
    return render(request, "auctions/index.html", {
        "amounts": Bid.objects.all(),
        "listings": listings,
        "categories": Category.objects.all(),
    })

# @login_required(login_url='login')    
def list_page(request, list_id):
    list_auction = Auction_listings.objects.get(id=list_id)
    categories = Category.objects.filter(id = list_id)
    comment_text = forms.Create_comment()
    bid_form = forms.Place_bid()
    if list_auction.fav_lists.filter(id=request.user.id).exists():
    # if request.user.is_authenticated:
        is_fav = Auction_listings(fav_check=True)
        # if Auction_listings.fav_lists.get(id=request.user.id).exists():
        #     fav = True
        return render(request, "auctions/auc_details.html", {
            "detail": list_auction,
            "cats":categories,
            "user": request.user,
            "comments": list_auction.comment.all(),
            "com_form":comment_text,
            "bid": bid_form,
            "is_fav":is_fav,
            # "rial": list_auction.listings.all(),
        })
    else:
        # list_auction = Auction_listings.objects.get(id =list_id)
        is_fav = Auction_listings(fav_check=False)
        return render(request, "auctions/auc_details.html", {
            "detail":list_auction,
            "cats":categories,
            "comments": list_auction.comment.all(),
            "com_form":comment_text,
            "bid": bid_form,
            "rial": list(Bid.objects.values_list('place_bid', flat=True)).pop(

            )
        })
        # return render(request, "auctions/auc_details.html", {
        #     "detail": list_auction,
        # })

        
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
            
@login_required(login_url='login')
def create_listing(request):
    form = forms.Create_listing(request.POST,request.FILES)
    # if request.user.is_authenticated:
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


@login_required(login_url='login')
def watch_list(request):
    # fav_w_l = Auction_listings.fav_lists.filter(id=request.user.id)
    return render (request,"auctions/watchlist.html", {
        "lists":  request.user.favorite.all().values(),
        # "fav":fav_w_l,
    })

@login_required(login_url='login')
def add_watch_list(request, list_id):
    list_auction = Auction_listings.objects.get(id=list_id)
    # request.user.favorite.add(list_auction)
    if list_auction.fav_lists.filter(id=request.user.id).exists():
        # list_auction.fav_lists.remove(request.user)
        request.user.favorite.remove(list_auction)
        request.user.save()
    else:
        request.user.favorite.add(list_auction)
        # list_auction.fav_lists.add(request.user)
        request.user.save()
    return HttpResponseRedirect(reverse("auctions_list", args=(list_auction.id,)))


def categories(request):
    # fav_w_l = Auction_listings.fav_lists.filter(id=request.user.id)
    return render (request,"auctions/category.html", {
        # "category":  request.user.favorite.all().values(),
        "categories":  Category.objects.all(),
        "msg":"Here is a list of all categories",
    })

def category_list(request, cats):
    get_cato = Auction_listings.objects.filter(auctions=cats)
    return render (request,"auctions/categoryList.html", {
        # "category":  request.user.favorite.all().values(),
        "title":cats,
        "pages": get_cato,
        # "pages": Category.objects.filter(category_type=get_cato),
        # "pages": Category.category_type.filter(id=list_id),
        # "pages": Category.objects.filter(id=list_id),
        "msg":"Here is a list of all categories",
    })

def bid(request,list_id):
    if request.user.is_authenticated:
        list_auction = Auction_listings.objects.get(pk=list_id)
        if request.method == 'POST':
            bid_digit = forms.Place_bid(request.POST)
            bds = list(Bid.objects.values_list('place_bid', flat=True))
            bds.sort()
            # bds = Bid.objects.get(place_bid=Bid.place_bid)
        if bid_digit.is_valid():
            if int(bid_digit['place_bid'].value()) > bds.pop():
                bid_dt = bid_digit.save(commit=False)
                # bid_dt.comment = comment_text["comment"]
                bid_dt.bid_on_auction = list_auction
                bid_dt.bid_by = request.user
                bid_dt.bid_count += 1
                bid_dt.save()
                # print(com_t)
            
                return HttpResponseRedirect(reverse("auctions_list", args=(list_auction.id,)))
            else:
                return render(request, "auctions/auc_details.html", {
                    "detail": list_auction,
                    # "cats":categories,
                    "user": request.user,
                    "comments": list_auction.comment.all(),
                    # "com_form":comment_text,
                    "bid": bid_digit,
                })
        return render (request,"auctions/auc_details.html", {
            "detail": list_auction,
            "user": request.user,
            "comments": list_auction.comment.all(),
            # "com_form":comment_text(),
            "bid": forms.Place_bid(request.POST ),
        })