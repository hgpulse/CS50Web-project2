from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Listing
from django.shortcuts import render
from .forms import ListingForm

from django.contrib.auth.decorators import login_required

# URL for MEDIA image

# import os
# from django.conf import settings

def index(request):
    all_entries = Listing.objects.all()
    # path = settings.MEDIA_ROOT
    # img_list = os.listdir(path + '/images')
    # context = {'images' : img_list}
    return render(request, "auctions/index.html", {'all_entries': all_entries} )


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

@login_required
def newlisting(request):
    """Process images uploaded by users"""
    if request.method == 'POST':
       
        form = ListingForm(request.POST, request.FILES)
        
        if form.is_valid():
            form.save()
            # Get the current instance object to display in the template
            img_obj = form.instance
            print(img_obj)
            return render(request, 'auctions/new_listing.html', {'form': form, 'img_obj': img_obj})
            
    else:
        
        form = ListingForm()
    return render(request, 'auctions/new_listing.html', {'form': form})

def listingpage(request, name):
    print(name)
    #query listing.name to get detail
    
    all_entries = Listing.objects.all()
    # path = settings.MEDIA_ROOT
    # img_list = os.listdir(path + '/images')
    # context = {'images' : img_list}
    return render(request, "auctions/listing_page.html", {
        'all_entries': all_entries,
        'name': name
        })