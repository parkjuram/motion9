from django.db import models
from datetime import datetime

class Category(models.Model):
    name = models.TextField(null=False)
    is_set = models.BooleanField(null=False, default=False)
    small_image = models.ImageField(null=True, upload_to='categoryimage/')

    def __unicode__(self):
        return '(%r)Category : name(%s) is_set(%r)' \
               % (self.id, self.name, self.is_set)

    def __str__(self):
        return unicode(self).encode('utf-8')

class Product(models.Model):
    name = models.TextField(unique=True)
    category = models.ForeignKey(Category)

    original_price = models.IntegerField(null=False, default=0)
    discount_price = models.IntegerField(null=False, default=0)
    fit_skin_type = models.CharField(max_length=30, blank=True)

    thumbnail_image = models.ImageField(null=True, upload_to='product/')
    video_url = models.URLField(blank=True)
    brandname = models.CharField(max_length=30, blank=True)
    maker = models.CharField(max_length=30, blank=True)
    country = models.CharField(max_length=30, blank=True)
    capacity = models.CharField(max_length=10, blank=True)
    description = models.TextField(blank=True)
    short_desc = models.CharField(max_length=100, blank=True)
    use_expired_date = models.CharField(max_length=50, blank=True)
    production_date = models.CharField(max_length=50, blank=True)
    usage = models.TextField(blank=True)
    ingredient = models.TextField(blank=True)
    judge_result = models.CharField(max_length=100, blank=True)
    precautions = models.TextField(blank=True)
    quality_guarantee_standard = models.CharField(max_length=100, blank=True)

    def __unicode__(self):
        return '(%r)Product : name(%s)' \
               % (self.id, self.name)

    def __str__(self):
        return unicode(self).encode('utf-8')

class ProductDescriptionImage(models.Model):
    product = models.ForeignKey(Product)
    image = models.ImageField(null=True, upload_to='product/desc/')

class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='product_image_set')
    image = models.ImageField(null=True, upload_to='product/image/')


# class Product(models.Model):
#     name = models.TextField(null=False)
#     category = models.ForeignKey(Category)
#     description = models.TextField(null=False, blank=True)
#     # description_img = models.ImageField(blank=True)
#     big_img_url = models.TextField(null=False, blank=True)
#     small_img_url = models.TextField(null=False, blank=True)
#     video_url = models.TextField(null=False, blank=True)
#     brandname = models.TextField(null=False, blank=True)
#     maker = models.TextField(null=False, blank=True)
#     capacity = models.TextField(null=False, blank=True)
#     original_price = models.IntegerField(null=False, default=0)
#     discount_price = models.IntegerField(null=False, default=0)
#     fit_skin_type = models.TextField(null=False, blank=True)
#     color_description = models.TextField(null=False, blank=True)
#     color_rgb = models.CharField(max_length=10, null=False, blank=True)
#     created = models.DateTimeField(auto_now_add=True, default=datetime.now)
#
#     def __unicode__(self):
#         return '(%r)Product : name(%s) category(%s) description(%s)' \
#                % (self.id, self.name, self.category.name, self.description)
#
#     def __str__(self):
#         return unicode(self).encode('utf-8')

class Set(models.Model):
    name = models.TextField(null=False)
    category = models.ForeignKey('Category')
    description = models.TextField(null=False, blank=True)
    big_img_url = models.TextField(null=False, blank=True)
    small_img_url = models.TextField(null=False, blank=True)
    discount_difference = models.IntegerField(null=False, default=0)

class Tag(models.Model):
    name = models.TextField(unique=True)

class SetTag(models.Model):
    set = models.ForeignKey('Set')
    tag = models.ForeignKey('Tag')

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

    class Meta:
        unique_together = (
            ("user", "set"))

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