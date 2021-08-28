from django import forms
from django.forms import fields
from . import models

class Create_listing(forms.ModelForm):
    class Meta:
        model = models.Auction_listings
        fields = ['auc_title', 'auc_details', 'auc_price', 'auctions', 'auc_image', 'auc_created_by']
        
        
class Create_comment(forms.ModelForm):
    class Meta:
        form_model = models.Comment
        form_fields = ['comment_on', 'comment']