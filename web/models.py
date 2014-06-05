from django.db import models
from datetime import datetime

class Category(models.Model):
    name = models.TextField(null=False)
    is_set = models.BooleanField(null=False, default=False)

    def __unicode__(self):
        return '(%r)Category : name(%s) is_set(%r)' \
               % (self.id, self.name, self.is_set)

    def __str__(self):
        return unicode(self).encode('utf-8')


class Product(models.Model):
    name = models.TextField(null=False)
    category = models.ForeignKey(Category)
    description = models.TextField(null=False, blank=True)
    big_img_url = models.TextField(null=False, blank=True)
    small_img_url = models.TextField(null=False, blank=True)
    video_url = models.TextField(null=False, blank=True)
    brandname = models.TextField(null=False, blank=True)
    maker = models.TextField(null=False, blank=True)
    capacity = models.TextField(null=False, blank=True)
    original_price = models.IntegerField(null=False, default=0)
    discount_price = models.IntegerField(null=False, default=0)
    fit_skin_type = models.TextField(null=False, blank=True)
    color_description = models.TextField(null=False, blank=True)
    color_rgb = models.CharField(max_length=10, null=False, blank=True)
    created = models.DateTimeField(auto_now_add=True, default=datetime.now)

    def __unicode__(self):
        return '(%r)Product : name(%s) category(%s) description(%s)' \
               % (self.id, self.name, self.category.name, self.description)

    def __str__(self):
        return unicode(self).encode('utf-8')

class Set(models.Model):
    name = models.TextField(null=False)
    category = models.ForeignKey('Category')
    description = models.TextField(null=False, blank=True)
    big_img_url = models.TextField(null=False, blank=True)
    small_img_url = models.TextField(null=False, blank=True)
    discount_difference = models.IntegerField(null=False, default=0)

class SetProduct(models.Model):
    set = models.ForeignKey('Set')
    product = models.ForeignKey('Product')
    created = models.DateTimeField(auto_now_add=True, default=datetime.now)

class ChangeableProduct(models.Model):
    set = models.ForeignKey('Set')
    product = models.ForeignKey('Product')

    class Meta:
        unique_together = (
            ("set", "product"))

class ChangeableProductInfo(models.Model):
    changeable_product = models.ForeignKey('ChangeableProduct')
    product = models.ForeignKey('Product')

    class Meta:
        unique_together = (
            ("changeable_product", "product"))

class CustomSet(models.Model):
    user = models.ForeignKey('users.UserProfile')
    set = models.ForeignKey('Set')
    created = models.DateTimeField(auto_now_add=True, default=datetime.now)

class CustomSetDetail(models.Model):
    custom_set = models.ForeignKey('CustomSet')
    original_product = models.ForeignKey('Product', related_name='get_custom_set_detail_from_original_product')
    new_product = models.ForeignKey('Product', related_name='get_custom_set_detail_from_new_product')

class BlogReview(models.Model):
    product = models.ForeignKey('Product')
    writer = models.TextField(null=False, blank=True)
    url = models.TextField(null=False, blank=True)
    big_img_url = models.TextField(null=False, blank=True)
    small_img_url = models.TextField(null=False, blank=True)
    review_created_time = models.DateTimeField(default=datetime.now)
    summary = models.TextField(null=False, blank=True)
    created = models.DateTimeField(auto_now_add=True, default=datetime.now)