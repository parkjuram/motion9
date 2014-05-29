from django.contrib import admin
from web.models import Category, Product, Set, CustomSet, CustomSetDetail

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Set)
admin.site.register(CustomSet)
admin.site.register(CustomSetDetail)
