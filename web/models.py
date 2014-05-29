from django.db import models
from datetime import datetime

class Category(models.Model):
    name = models.TextField(null=False)
    is_set = models.BooleanField(null=False, default=False)

class Product(models.Model):
    name = models.TextField(null=False)
    category = models.ForeignKey(Category)
    description = models.TextField(null=True)
    big_img_url = models.TextField(null=True)
    small_img_url = models.TextField(null=True)
    video_img_url = models.TextField(null=True)
    brandname = models.TextField(null=True)
    maker = models.TextField(null=True)
    capacity = models.TextField(null=True)
    original_price = models.IntegerField(null=False, default=0)
    discount_price = models.IntegerField(null=False, default=0)
    fit_skin_type = models.TextField(null=True)

class Set(models.Model):
    name = models.TextField(null=False)
    category = models.ForeignKey('Category')
    description = models.TextField(null=True)
    big_img_url = models.TextField(null=True)
    small_img_url = models.TextField(null=True)
    discount_difference = models.IntegerField(null=False, default=0)

class CustomSet(models.Model):
    user = models.ForeignKey('users.UserProfile')
    set = models.ForeignKey('Set')
    created = models.DateTimeField(auto_now_add=True, default=datetime.now)

class CustomSetDetail(models.Model):
    custom_set = models.ForeignKey('CustomSet')
    original_product = models.ForeignKey('Product', related_name='get_custom_set_detail_from_original_product')
    new_product = models.ForeignKey('Product', related_name='get_custom_set_detail_from_new_product')