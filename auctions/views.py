from django.contrib.auth import REDIRECT_FIELD_NAME, authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.db.models import F
from django.urls import reverse
from datetime import datetime
from . import forms

from .models import *


def index(request):
    listings = Auction.objects.all().order_by('-publication_date')
    return render(request, "auctions/index.html", {
        "amounts": Bid.objects.all(),
        "listings": listings,
        "categories": Category.objects.all(),
    })

# @login_required(login_url='login')    
def view_item(request, list_id):
    list_auction = Auction.objects.get(id=list_id)
    categories = Category.objects.filter(id = list_id)
    comment_text = forms.Create_comment()
    bid_form = forms.Place_bid()
    if list_auction.favorite_item.filter(id=request.user.id).exists():
        is_fav = True
        return render(request, "auctions/item_description.html", {
            "detail": list_auction,
            "cats":categories,
            "user": request.user,
            "comments": list_auction.comment.all(),
            "com_form":comment_text,
            "bid": bid_form,
            "is_fav":is_fav,
            "total_bid": len(Bid.objects.filter(bid_on_auction=list_auction)),
        })
    else:
        return render(request, "auctions/item_description.html", {
            "detail":list_auction,
            "cats":categories,
            "comments": list_auction.comment.all(),
            "com_form":comment_text,
            "bid": bid_form,
            "total_bid": len(Bid.objects.filter(bid_on_auction=list_auction)),
        })
        

        
def comment(request,list_id):
    list_auction = Auction.objects.get(pk=list_id)
    if request.method == 'POST':
        comment_text = forms.Create_comment(request.POST)
        if comment_text.is_valid():                                                                                                                                         
            com_t = comment_text.save(commit=False)
            com_t.comment_on = list_auction
            com_t.comment_by = request.user
            com_t.save()
        
            return HttpResponseRedirect(reverse("view_item", args=(list_auction.id,)))
        else:
            return render(request, "auctions/item_description.html", {
                "detail": list_auction,
                "user": request.user,
                "comments": list_auction.comment.all(),
                "com_form":comment_text,
            })
    return render (request,"auctions/item_description.html", {
        "detail": list_auction,
        "user": request.user,
        "comments": list_auction.comment.all(),
        "com_form":comment_text()
    })
            
@login_required(login_url='login')
def new_item(request):
    form = forms.Create_item(request.POST,request.FILES)
    if request.method == "POST":
        form = form
        if form.is_valid():
            form_list = form.save(commit=False)
            form_list.item_owner = request.user
            form_list.save()
            form.save_m2m()
        else:
            return render(request, "auctions/new_item.html",{
                "form":form,
            })        
    return render (request,"auctions/new_item.html", {
        "form": forms.Create_item()
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
    return render (request,"auctions/watchlist.html", {
        "pages":  request.user.favorite.all(),
    })

@login_required(login_url='login')
def add_watch_list(request, list_id):
    list_auction = Auction.objects.get(id=list_id)
    if list_auction.favorite_item.filter(id=request.user.id).exists():
        list_auction.fav_check = False 
        list_auction.save()
        request.user.favorite.remove(list_auction)
        request.user.save()
    else:
        request.user.favorite.add(list_auction)
        list_auction.fav_check = True
        list_auction.save()
        request.user.save()
    return HttpResponseRedirect(reverse("view_item", args=(list_auction.id,)))


def categories(request):
    return render (request,"auctions/category.html", {
        "categories":  Category.objects.all(),
    })

def category_list(request, cats):
    get_item_perCategory = Auction.objects.filter(item_category=cats)
    return render (request,"auctions/categoryList.html", {
        "title":Category.objects.get(id = cats),
        "pages": get_item_perCategory,
    })

@login_required(login_url='login')
def bid(request,list_id):
    list_auction = Auction.objects.get(pk=list_id)
    comment_text = forms.Create_comment()
    if request.method == 'POST':
        bid_digit = forms.Place_bid(request.POST)
        bds = list(Bid.objects.values_list('place_bid', flat=True))
        bds.sort(reverse=True)
        if bid_digit.is_valid():
            if Bid.objects.filter(bid_on_auction=list_auction).exists():
                last_bid = float(Bid.objects.filter(bid_on_auction=list_auction).last().place_bid)
                if int(bid_digit['place_bid'].value()) > last_bid and list_auction.starting_price:
                    bid_dt = bid_digit.save(commit=False)
                    bid_dt.bid_on_auction = list_auction
                    bid_dt.bid_by = request.user
                    bid_dt.save()
                
                    return HttpResponseRedirect(reverse("view_item", args=(list_auction.id,)))
                else:
                    return render(request, "auctions/item_description.html", {
                        "detail": list_auction,
                        "error": f"number must be greater than {list_auction.starting_price} and { last_bid } ",
                        "user": request.user,
                        "comments": list_auction.comment.all(),
                        "com_form":comment_text,
                        "bid": bid_digit,
                        "total_bid": len(Bid.objects.filter(bid_on_auction=list_auction))
                    })
            
            else:
                if int(bid_digit['place_bid'].value()) > list_auction.starting_price:
                    bid_dt = bid_digit.save(commit=False)
                    bid_dt.bid_on_auction = list_auction
                    bid_dt.bid_by = request.user
                    bid_dt.save()
                
                    return HttpResponseRedirect(reverse("view_item", args=(list_auction.id,)))
                else:
                    return render(request, "auctions/item_description.html", {
                        "detail": list_auction,
                        "error": f"number must be greater than {list_auction.starting_price} ",
                        "user": request.user,
                        "comments": list_auction.comment.all(),
                        "com_form":comment_text,
                        "bid": bid_digit,
                        "total_bid": len(Bid.objects.filter(bid_on_auction=list_auction))
                    })
        else:
            return render(request, "auctions/item_description.html", {
                "detail": list_auction,
                "user": request.user,
                "comments": list_auction.comment.all(),
                "bid": bid_digit,
            })
    else:
        return render (request,"auctions/item_description.html", {
            "detail": list_auction,
            "user": request.user,
            "comments": list_auction.comment.all(),
            "bid": forms.Place_bid(),
        })

@login_required(login_url='login')
def close_bid(request,list_id):
    list_auction = Auction.objects.get(pk=list_id)
    if request.user == list_auction.item_owner:
        list_auction.bid_winner = str(Bid.objects.filter(bid_on_auction=list_auction).last().bid_by)
        list_auction.active_item = False
        list_auction.save()
        return HttpResponseRedirect(reverse("view_item", args=(list_auction.id,)))
    else:
        return HttpResponseRedirect(reverse("view_item", args=(list_auction.id,)))