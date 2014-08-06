from django.contrib import admin

from .models import UserProfile, Interest, Cart, Purchase, CustomSet, CustomSetDetail

class CustomSetAdmin(admin.ModelAdmin):
    list_display = ('user', 'set', 'is_active', 'created')
    list_editable = ('is_active',)
    list_display_links = ('user','set',)

admin.site.register(CustomSet, CustomSetAdmin)

class CustomSetDetailAdmin(admin.ModelAdmin):
    list_display = ('custom_set','original_product','new_product')
    # list_editable = ('is_active',)
    list_display_links = ('custom_set','original_product','new_product',)

admin.site.register(CustomSetDetail, CustomSetDetailAdmin)

admin.site.register(UserProfile)
admin.site.register(Interest)
admin.site.register(Cart)
admin.site.register(Purchase)