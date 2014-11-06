from django.contrib import admin

from .models import UserProfile, Interest, Cart, Purchase, CustomSet, CustomSetDetail, Payment, BeforePayment
from users.models import UserSurvey


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
    list_display = ('user', 'name', 'phone', 'postcode', 'basic_address', 'detail_address', 'sex', 'age', 'skin_type', 'skin_color', 'mileage')
    list_editable = ('name', 'phone', 'postcode', 'basic_address', 'detail_address', 'sex', 'age', 'skin_type', 'skin_color', 'mileage',)
    list_display_links = ('user',)

admin.site.register(UserProfile, UserProfileAdmin)

class PurchaseAdmin(admin.ModelAdmin):
    list_display = ('user', 'payment', 'price', 'product', 'set', 'custom_set', 'type', 'item_count', 'created')
    list_editable = ('price', 'type', 'item_count',)
    list_display_links = ('user', 'payment', 'product', 'set', 'custom_set',)

admin.site.register(Purchase, PurchaseAdmin)

class PaymentAdmin(admin.ModelAdmin):
    list_display = ('user', 'service_id', 'order_id', 'order_date', 'transaction_id', 'auth_amount',
                    'auth_date', 'response_code', 'response_message', 'detail_response_code', 'detail_response_message',
                    'name', 'status', 'shipping_number', 'phone', 'postcode', 'address', 'shipping_requirement', 'mileage', 'created')

    list_editable = ('service_id', 'order_id', 'order_date', 'transaction_id', 'auth_amount',
                     'auth_date', 'response_code', 'response_message', 'detail_response_code', 'detail_response_message',
                     'name', 'status', 'shipping_number', 'phone', 'postcode', 'address', 'shipping_requirement', 'mileage',)

    list_display_links = ('user',)

admin.site.register(Payment, PaymentAdmin)

class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'set', 'custom_set', 'type', 'item_count', 'order_id', 'created')
    list_editable = ('custom_set', 'type', 'item_count', 'order_id',)
    list_display_links = ('user', 'product', 'set',)

admin.site.register(Cart, CartAdmin)

class BeforePaymentAdmin(admin.ModelAdmin):
    list_display = ('user', 'order_id', 'name', 'phone', 'postcode', 'address', 'shipping_requirement', 'mileage', 'created')
    list_editable = ('name', 'phone', 'postcode', 'address', 'shipping_requirement', 'mileage',)
    list_display_links = ('user',)

admin.site.register(BeforePayment, BeforePaymentAdmin)


class UserSurveyAdmin(admin.ModelAdmin):
    list_display = ('user', 'survey_item', 'survey_item_option')
    list_display_links = ('user', 'survey_item', 'survey_item_option',)

admin.site.register(UserSurvey, UserSurveyAdmin)


admin.site.register(Interest)



