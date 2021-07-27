from django.contrib import admin
from .models import *

# Register your models here.
class Auction_listings_admin(admin.ModelAdmin):
    list_display = ("id", "auc_title", "auc_details", "auc_price", "auc_created_by")    
    
class Comment_admin(admin.ModelAdmin):
    list_display = ("id", "comment_by", "comment_on", "comment_date_published", "comment")   
    
class Bid_admin(admin.ModelAdmin):
    list_display = ("id", "bid_by", "bid_on_auction", "bid_amount")   

admin.site.register(User)
admin.site.register(Auction_listings)
admin.site.register(Comment, Comment_admin)
admin.site.register(Bid, Bid_admin)
