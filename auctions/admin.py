from django.contrib import admin
from .models import *

# Register your models here.
class Auction_admin(admin.ModelAdmin):
    list_display = ("id", "item_name", "item_description", "starting_price", "item_owner", "favorite_item")    
    
class Comment_admin(admin.ModelAdmin):
    list_display = ("id", "comment_on", "comment")   
                                                                                                                                                                                                                                                                    
class Bid_admin(admin.ModelAdmin):
    list_display = ("id", "bid_by", "bid_on_auction", "place_bid")   
    

class Category_admin(admin.ModelAdmin):
   list_display = ("id","category_type" )

admin.site.register(User)
admin.site.register(Auction)
admin.site.register(Comment, Comment_admin)
admin.site.register(Bid, Bid_admin)
admin.site.register(Category,Category_admin)
