from django.contrib import admin
from users.models import UserProfile, Interest

from web.models import Category, Product, Set, CustomSet, CustomSetDetail

admin.site.register(UserProfile)
admin.site.register(Interest)
# Register your models here.
