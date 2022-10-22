from django import forms
from django.forms import fields
from . import models

class Create_listing(forms.ModelForm):
    class Meta:
        model = models.Auction_listings
        fields = ['auc_title', 'auc_details', 'auc_price', 'auctions', 'auc_image']
        widgets = {
            'auc_details': forms.Textarea(attrs={'cols': 50, 'rows': 5}),
        }
        labels = {
            'auc_title': ('Item'),
            'auc_details':('Description'),
            'auc_price':('Price'),
            'auctions':('Category'),
            'auc_image':('Choose a Picture of the Item')
        }
        help_texts = {
            'auc_title': ('Item name like: Watch, Book, etc.'),
            'auc_details':("Describe the Item's feture"),
            'auc_price':('Staring Bid'),
        }
        
        
class Create_comment(forms.ModelForm):
    class Meta:
        model = models.Comment
        fields = ['comment']


class Place_bid(forms.ModelForm):
    class Meta:
        model = models.Bid
        fields = ['place_bid']
