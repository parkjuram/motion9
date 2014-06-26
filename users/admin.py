from django.contrib import admin

from .models import UserProfile, Interest, Cart, Purchase, CustomSet, CustomSetDetail

admin.site.register(UserProfile)
admin.site.register(Interest)
admin.site.register(Cart)
admin.site.register(Purchase)
admin.site.register(CustomSet)
admin.site.register(CustomSetDetail)