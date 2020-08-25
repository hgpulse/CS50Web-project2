from django.contrib.auth.models import AbstractUser
from django.db import models

from django.conf import settings
from django.utils.translation import ugettext_lazy as _

# modelsForm
from django.forms import ModelForm, SelectDateWidget, TextInput

# revers URL
from django.urls import reverse

class User(AbstractUser):
    pass

class watchlist(models.Model):
    user = models.CharField(max_length=100, blank=True, null=True)
    listing_id = models.IntegerField(blank=True, null=True)
    def __str__(self):
        return f"{self.user} for listing ID: {self.listing_id}"

    
    def get_absolute_url(self):
        return reverse('listingpage', kwargs={'pk': self.listing_id})

class Listing(models.Model):
    INACTIVE = 0
    ACTIVE = 1

    STATUS = (
        (INACTIVE, _('Inactive')),
        (ACTIVE, _('Active')),
    )
    CAT_TYPE = (
        ('None', 'None'),
        ('Gold', 'Brand New'),
        ('Silver', 'Used with love'),
        ('Bronze', 'Used with love for a longtime'),
        
    )
    name = models.CharField(max_length=50)
    initial_price = models.IntegerField()
    # can get via sessions ID
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default= 1, on_delete=models.CASCADE)
    category = models.CharField(max_length=64, choices=CAT_TYPE, default=CAT_TYPE[0][0], blank=True, null=True)
    description = models.CharField(max_length=100)
    date = models.DateTimeField(auto_now=True)
    active = models.IntegerField(default=1, choices=STATUS)
    image = models.ImageField(upload_to='images', default='images', blank=True, null=True)
    watchlist = models.ForeignKey(watchlist , on_delete=models.CASCADE, blank=True, null=True)
    
    def __str__(self):
        return f"{self.name} at {self.date} for {self.initial_price}"

    def __unicode__(self):
        return self.name



class Bid(models.Model):
    user = models.CharField(max_length=100, blank=True, null=True)
    price = models.IntegerField()
    listing_id = models.IntegerField(blank=True, null=True)
    date = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.price

    def __str__(self):
        return f"{self.price} on the {self.date} by {self.user}"

class Comment(models.Model):
    user = models.CharField(max_length=100, blank=True, null=True)
    title = models.CharField(max_length=32)
    content = models.CharField(max_length=100)
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f" {self.title} on the {self.date}"

    def __unicode__(self):
        return self.title

class ClientAccount(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default= 1, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now=True)
    watchlist = models.ForeignKey(watchlist, on_delete=models.CASCADE, blank=True, null=True)
    bid = models.ForeignKey(Bid, on_delete=models.CASCADE, blank=True, null=True)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, blank=True, null=True)
    listing_own = models.ForeignKey(Listing, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return f" {self.user} created {self.created}"
    
    def __unicode__(self):
        return self.user
class ListingForm(ModelForm):

    class Meta:
        model = Listing
        fields = ('__all__')
        exclude =('user','watchlist',)
        widgets = {
            'name': TextInput(attrs={'placeholder':'Title'}),
            'description': TextInput(attrs={'placeholder':'Description'}),
            'initial_price': TextInput(attrs={'placeholder':'Price'}),
            'date': SelectDateWidget()
        }


class BidForm(ModelForm):
    class Meta:
        model = Bid
        fields = ('__all__')
        
        
        