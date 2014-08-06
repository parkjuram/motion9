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

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'phone', 'address', 'sex', 'age', 'skin_type', 'skin_color', 'mileage')
    list_editable = ('name', 'phone', 'address', 'sex', 'age', 'skin_type', 'skin_color', 'mileage',)
    list_display_links = ('user',)

admin.site.register(UserProfile, UserProfileAdmin)

class PurchaseAdmin(admin.ModelAdmin):
    list_display = ('user', 'payment', 'price', 'address', 'product', 'set', 'custom_set', 'type', 'item_count', 'status', 'shipping_number', 'created')
    list_editable = ('price', 'address', 'type', 'item_count', 'status', 'shipping_number',)
    list_display_links = ('user', 'payment', 'product', 'set', 'custom_set',)

admin.site.register(Purchase, PurchaseAdmin)

admin.site.register(Interest)
admin.site.register(Cart)
