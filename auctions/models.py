from django.contrib.auth.models import AbstractUser
from django.db import models

from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import gettext_lazy as _
# modelsForm
from django.forms import ModelForm, SelectDateWidget, TextInput



# revers URL
from django.urls import reverse

class User(AbstractUser):
    pass

class Comment(models.Model):
    user_id = models.IntegerField(blank=True, null=True)
    listing_id = models.IntegerField(blank=True, null=True)
    content = models.CharField(max_length=100)
    date = models.DateTimeField(auto_now=True)
    author = models.CharField(max_length=100)

    def __str__(self):
        return f"  {self.listing_id} wrote {self.content} on the {self.date}"

    def __unicode__(self):
        return self.listing_id

class watchlist(models.Model):
    user = models.IntegerField(blank=True, null=True)
    listing_id = models.IntegerField(blank=True, null=True)
    product_title = models.CharField(max_length=100)
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
    
   
    HEALTH = 1
    MOTOR = 2
    FOOD = 3
    
    
    CAT_TYPE = (
        (HEALTH, _('HEALTH')),
        (MOTOR, _('MOTOR')),
        (FOOD, _('FOOD')),
        
    )
    name = models.CharField(max_length=50)
    initial_price = models.IntegerField()
    # can get via sessions ID
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default= 1, on_delete=models.CASCADE)
    category = models.IntegerField(choices=CAT_TYPE, default=None, blank=True, null=True)
    description = models.CharField(max_length=100)
    date = models.DateTimeField(auto_now=True)
    active = models.IntegerField(default=1, choices=STATUS)
    image = models.ImageField(upload_to='images', default='images', blank=True, null=True)
    watchlist = models.ForeignKey(watchlist , on_delete=models.CASCADE, blank=True, null=True)
    winner = models.IntegerField(blank=True, null=True)
    comment = models.ManyToManyField(Comment , blank=True)
    
    def __str__(self):
        return f"{self.name} at {self.date} for {self.initial_price}"

    def __unicode__(self):
        return self.name
    
    def comments_all(self):
        return ', '.join([a.comment_all for a in self.comment.all()])
    comments_all.short_description = "comments_all"

    def is_upperclass(self):
        return self.category in {self.GOLD, self.SILVER, self.BRONZE }
    
    # def __str__(self):
    #     return self.get_category_display()

class Bid(models.Model):
    user = models.CharField(max_length=100, blank=True, null=True)
    price = models.IntegerField()
    listing_id = models.IntegerField(blank=True, null=True)
    date = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.price

    def __str__(self):
        return f"{self.price} on the {self.date} by {self.user}"




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


        
        
        