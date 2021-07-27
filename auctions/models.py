from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db import models


class User(AbstractUser):
    pass

class Auction_listings(models.Model):
    auc_title = models.CharField(max_length=50)
    auc_details = models.CharField(max_length=250)
    auc_price = models.IntegerField()
    auc_date_published = models.DateTimeField(auto_now_add=True)
    auc_created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="creator", blank=True)
    auc_image = models.ImageField(default='rose.jpg', blank=True)
    
    def __str__(self):
        return f"{self.auc_title} {self.auc_details} {self.auc_date_published} "
        
class Bid(models.Model):
    bid_by = models.ForeignKey(User, related_name="user", on_delete=models.CASCADE)
    bid_on_auction = models.ForeignKey(Auction_listings, related_name="listings", on_delete=models.CASCADE)
    # think about bid amount
    bid_amount = models.ForeignKey(Auction_listings, on_delete=models.CASCADE, related_name="bid")
    
    def __str__(self):
        return f"{self.bid_by} {self.bid_amount} {self.bid_on_auction}"
    
class Comment(models.Model):
    comment_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="commentor", blank=False)
    comment_on = models.ForeignKey( Auction_listings, related_name="comment", on_delete=models.CASCADE)
    comment = models.CharField(max_length=600)
    comment_date_published = models.DateTimeField()
    
    def __str__(self):
        return f"{self.comment_by} {self.comment} {self.comment_date_published} {self.comment_on}"
        