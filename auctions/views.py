from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Listing, ListingForm, watchlist, WatchForm
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


# class ContactView(FormView):
#     template_name = 'watchcreate.html'
#     form_class = WatchForm
#     success_url = '/thanks/'

#     def form_valid(self, form):
#         # This method is called when valid form data has been POSTed.
#         # It should return an HttpResponse.
#         print("valid")
#         return super().form_valid(form)

class watchcreate(CreateView):
    model = watchlist
    fields = ['owner','product' ]
    
    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
       
        print("valid")
        return super().form_valid(form)

class WatchListView(ListView):

    model = watchlist
    paginate_by = 100  # if pagination is desired

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context