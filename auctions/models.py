from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db import models

class User(AbstractUser):
    pass


class Category(models.Model):
    category_type = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.category_type}"

    # def get_absolute_url(self):
    #     return reverse("categoriesList", args=[str(self.id)])

class Auction_listings(models.Model):
    auc_title = models.CharField(max_length=50)
    auc_details = models.CharField(max_length=250)
    auc_price = models.PositiveIntegerField(blank=False)
    auc_date_published = models.DateTimeField(auto_now_add=True)
    auc_created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="creator", blank=True)
    auc_image = models.ImageField(default='rose.jpg', blank=False)
    auctions = models.ManyToManyField(Category, blank= True, related_name="category")
    winner = models.CharField(max_length=250, blank=True)
    active_auction = models.BooleanField(default=True)
    fav_lists = models.ManyToManyField(User, blank=True, related_name="favorite")
    fav_check = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.auc_title} "

        
class Bid(models.Model):
    bid_by = models.ForeignKey(User, related_name="user", on_delete=models.CASCADE)
    bid_on_auction = models.ForeignKey(Auction_listings, related_name="listings", on_delete=models.CASCADE)
    place_bid = models.PositiveIntegerField(blank=True)
    
    def __str__(self):
        return f"{self.bid_by} ${self.place_bid} {self.bid_on_auction}"
    
class Comment(models.Model):
    comment_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="commentor", blank=False)
    comment_on = models.ForeignKey( Auction_listings, related_name="comment", on_delete=models.CASCADE)
    comment = models.CharField(max_length=600)
    comment_date_published = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.comment}"
        
# class Watchlist(models.Model):
#     # first = models.CharField(max_length=64)
#     # last = models.CharField(max_length=64)

#     def __str__(self):
#         return f"{self.lists}"
