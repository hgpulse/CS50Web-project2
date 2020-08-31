from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, redirect
from django.urls import reverse

from .models import User, Listing, ListingForm, watchlist, Bid, BidForm, Comment
from django.shortcuts import render


from django.contrib.auth.decorators import login_required

from django.views.generic import ListView, DetailView, FormView
from django.utils import timezone

from django.views.generic.edit import CreateView, SingleObjectMixin

from django.db.models import Max

# import os
# from django.conf import settings

def index(request):
    all_entries = Listing.objects.all()

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
       
        form = ListingForm(request.POST, request.FILES, request.user)

        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            if not request.user == instance.user:
                raise Http404
            instance.save()
            
            print("valid")
            
            img_obj = form.instance
            
            return render(request, 'auctions/new_listing.html', {'form': form, 'img_obj': img_obj})
            
    else:
        
        form = ListingForm()
    return render(request, 'auctions/new_listing.html', {'form': form})

class listingpage(DetailView):
    model = Listing
    context_object_name = 'listing'
    template_name = 'auctions/listing_page.html'


@login_required
def watchcreate(request,pk):
    listing_id = pk
    if request.method == 'POST':
        # store the input
        owner = request.POST["owner"]
        product = request.POST["product"]
        
        # query existing object if exist delete
        if watchlist.objects.filter(user=owner).exists() and watchlist.objects.filter(listing_id=product).exists():
            
            d = watchlist.objects.filter(listing_id=product).delete()
            return redirect("listingpage", pk=listing_id)

        else:
            # create the object
            b = watchlist(user=owner, listing_id=product)
            b.save()
          
            return redirect("listingpage", pk=listing_id)
        
        
    else:
            
       return redirect("listingpage", pk=listing_id)

@login_required
def bidcreate(request,pk):
    
    listing_id = pk
    
    if request.method == 'POST':
        # store the input
        # owner = request.POST["owner"]
        # bid = request.POST["bid"]
        
        #query actual listing price with get
        ListingLive = Listing.objects.get(pk=listing_id)
        
        #store the initial price
        ListingPrice = ListingLive.initial_price
        
        print(f"live: {ListingPrice}")
        
        owner = request.POST["owner"]
        bid = float(request.POST["bid"])
        print(owner)
        print(bid)
        print(pk)
        
        # check if there is a bid for the Listing PK
        args = Bid.objects.filter(listing_id=pk)
        
        # compare to initial price
        if bid >= ListingPrice:
            # create the bid
            b0 = Bid(user=owner, price=bid, listing_id=listing_id)
            b0.save()
            #update listing initial price
            Listing.objects.filter(pk=listing_id).update(initial_price=bid,winner=owner)
            return HttpResponse('<h1>your bid: %s is done</h1>' % bid)
            return redirect("listingpage", pk=listing_id)

        elif args:
            #if yes select the winner and update the price in listing
            args.aggregate(Max('price')) # {'rating__max': 5}
            winner = args.order_by('-price')[0]
            print(f"actual winner {winner.user}")
            #update listing initial price
            Listing.objects.filter(pk=listing_id).update(initial_price=bid,winner=owner)
            # create the bid
            b0 = Bid(user=owner, price=bid, listing_id=listing_id)
            b0.save()
            print(ListingLive.initial_price)


        return HttpResponse('<h1>Your offer is too low actual price is %s</h1>' % ListingPrice)

        return redirect("listingpage", pk=listing_id)
     

    return redirect("listingpage", pk=listing_id)   
       
@login_required
def auctionclose(request,pk):
    
    listing_id = pk
    
    if request.method == 'POST':
       
        # get the object
        ListingLive = Listing.objects.get(pk=listing_id)
        
        #store the owner of the auction
        ListingUser = ListingLive.user
        
        print(f"live: {ListingUser}")
        
        owner = request.POST["owner"]
        
        
        print(f"live: {ListingUser} egual {owner}")
        #update listing initial price
        Listing.objects.filter(pk=listing_id).update(active=0)
        return redirect("index")
     

    return redirect("index")   

@login_required
def addcomment(request,pk):
    
    listing_id = pk
    
    if request.method == 'POST':
       
        # get the object
        getListing = Listing.objects.get(pk=listing_id)
        
        #store the owner of the auction
        ListingUser = getListing.user
        
        print(f"live: {getListing}")
        
        owner = request.POST["owner"]
        comment = request.POST["comment"]
        
        
        print(f"live: {owner} user ID {owner} said {comment}")
        # Create the comment
        #c0 = Comment(user_id=owner, content=comment, listing_id=listing_id)
        #c0.save()

        # add the comment to the listing ID
        print(getListing)
        # Create and add a Publication to an Article in one step using create():
        new_publication = getListing.comment.create(content=comment, user_id=owner, listing_id=listing_id)
        # Listing.objects.filter(pk=listing_id).update(comment=c0)
       
        return redirect ("listingpage", pk=listing_id)
     

    return redirect ("listingpage", pk=listing_id)
    

class WatchListView(ListView):

    model = watchlist
    paginate_by = 100  # if pagination is desired

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context