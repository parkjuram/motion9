from django.contrib import admin

from .models import UserProfile, Interest, Cart, Purchase

admin.site.register(UserProfile)
admin.site.register(Interest)
admin.site.register(Cart)
admin.site.register(Purchase)
