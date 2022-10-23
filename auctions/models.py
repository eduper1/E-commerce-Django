from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db import models

class User(AbstractUser):
    pass


class Category(models.Model):
    category_type = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.category_type}"



class Auction(models.Model):
    item_name = models.CharField(max_length=50)
    item_description = models.CharField(max_length=250)
    starting_price = models.PositiveIntegerField(blank=False)
    publication_date = models.DateTimeField(auto_now_add=True)
    item_owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="creator", blank=True)
    item_image = models.ImageField(default='rose.jpg', blank=False)
    item_category = models.ManyToManyField(Category, blank= True, related_name="category")
    bid_winner = models.CharField(max_length=250, blank=True)
    active_item = models.BooleanField(default=True)
    favorite_item = models.ManyToManyField(User, blank=True, related_name="favorite")
    fav_check = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.item_name} "

        
class Bid(models.Model):
    bid_by = models.ForeignKey(User, related_name="user", on_delete=models.CASCADE)
    bid_on_auction = models.ForeignKey(Auction, related_name="listings", on_delete=models.CASCADE)
    place_bid = models.PositiveIntegerField(blank=True)
    
    def __str__(self):
        return f"{self.bid_by} ${self.place_bid} {self.bid_on_auction}"
    
class Comment(models.Model):
    comment_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="commentor", blank=False)
    comment_on = models.ForeignKey( Auction, related_name="comment", on_delete=models.CASCADE)
    comment = models.CharField(max_length=600)
    comment_date_published = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.comment}"
        
