from django import forms
from django.forms import fields
from . import models

class Create_item(forms.ModelForm):
    class Meta:
        model = models.Auction
        fields = ['item_name', 'item_description', 'starting_price', 'item_category', 'item_image']
        widgets = {
            'item_description': forms.Textarea(attrs={'cols': 50, 'rows': 5}),
        }
        labels = {
            'item_name': ('Item'),
            'item_description':('Description'),
            'starting_price':('Price'),
            'item_category':('Category'),
            'item_image':('Choose a Picture of the Item')
        }
        help_texts = {
            'item_name': ('Item name like: Watch, Book, etc.'),
            'item_description':("Describe the Item's feture"),
            'starting_price':('Starting Bid'),
            'item_category':('Hold down “Control”, or “Command” on a Mac, to select more than one. ')
        }
        
        
class Create_comment(forms.ModelForm):
    class Meta:
        model = models.Comment
        fields = ['comment']
        widgets = {
            'comment': forms.Textarea(attrs={'cols': 50, 'rows': 5}),
        }


class Place_bid(forms.ModelForm):
    class Meta:
        model = models.Bid
        fields = ['place_bid']
