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
    # path("listing-page/<int:pk>/add-to-watch-list", watchcreate.as_view(), name="watchcreate"),
    path('watch-list/', WatchListView.as_view(), name='watch-list')

    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
