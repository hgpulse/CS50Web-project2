from django.contrib import admin

from .models import Listing, User
# Register your models here.
admin.site.register(Listing)
admin.site.register(User)