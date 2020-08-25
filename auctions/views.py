from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render
from django.urls import reverse

from .models import User, Listing, ListingForm, watchlist, Bid
from django.shortcuts import render


from django.contrib.auth.decorators import login_required

from django.views.generic import ListView, DetailView, FormView
from django.utils import timezone

from django.views.generic.edit import CreateView

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
            # form.save
            # store the user instance 
            
        
            #fs.save()
            # Get the current instance object to display in the template
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
    # pk = request.GET['pk']
    if request.method == 'POST':
        # store the input
        owner = request.POST["owner"]
        product = request.POST["product"]
        
        # query existing object if exist delete
        if watchlist.objects.filter(user=owner).exists() and watchlist.objects.filter(listing_id=product).exists():
            
            d = watchlist.objects.filter(listing_id=product).delete()
            return HttpResponse("%s Remove from watchlist." % product)

        else:
            # create the object
            b = watchlist(user=owner, listing_id=product)
            b.save()
            
            return HttpResponse("%s Add to watchlist." % product)
        
        
    else:
            
       return HttpResponse("nothing to do !!!!.")

@login_required
def bidcreate(request,pk):
   
    if request.method == 'POST':
        # store the input
        owner = request.POST["owner"]
        bid = request.POST["bid"]
        form = ListingForm(request.POST)
        if form.is_valid():
             print(owner)
             print(bid)
        
        # if bid.objects.filter(user=owner).exists() and bid.objects.filter(price=bid).exists():
            
        #     d = watchlist.objects.filter(price=bid).delete()
        #     return HttpResponse("%s Remove from watchlist." % product)

        # else:
            # create the object
        b = bid(user=owner, price=bid)
        b.save()
            
        return HttpResponse("%s Add to Bid." % bid)
        
        
    else:
            
       return HttpResponse("nothing to do !!!!.")
# class watchcreate(CreateView):
#     model = watchlist
#     fields = ['product', 'owner']
    
#     def get_initial(self):
#         # Retrieve initial data for the form. By default, returns a copy of initial.
#         print(self.request.user)
    
#     # def get_context_data(self, **kwargs):
#     #     # Call the base implementation first to get a context
#     #     context = super().get_context_data(**kwargs)
#     #     # Add in a QuerySet of all the books
#     #     context['watchlist'] = watchlist.objects.all()
#     #     return context
   

#     def form_valid(self, form):
#         # This method is called when valid form data has been POSTed.
#         # It should return an HttpResponse.
#         form.instance.owner = self.request.user
#         # form.instance.product = self.request.pk

#         return super().form_valid(form)

class WatchListView(ListView):

    model = watchlist
    paginate_by = 100  # if pagination is desired

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context