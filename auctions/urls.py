from django.urls import path
from . import views
from auctions.views import listingpage, WatchListView
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("new-listing", views.newlisting, name="newlisting"),
    path("active-listing", views.index, name="index"),
    path("listing-page/<int:pk>/", listingpage.as_view(), name="listingpage"),
    path("listing-page/<int:pk>/watch-create/", views.watchcreate, name="watchcreate"),
    path('watchlist/', WatchListView.as_view(), name='watch-list'),
    path("listing-page/<int:pk>/bid-create/", views.bidcreate, name="bidcreate"),
    path("listing-page/<int:pk>/auction-close/", views.auctionclose, name="auctionclose"),
    path("listing-page/<int:pk>/add-comment/", views.addcomment, name="addcomment"),
    #path('categories/', categories.as_view(), name='categories'),
    path("categories/", views.categories, name="categories"),
    path("categories/<int:cat>", views.catfilter, name="catfilter"),
    path("closed-listing", views.closed, name="closed"),

   
   

    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
