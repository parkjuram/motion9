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

    is_active = models.BooleanField(default=True)

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

class Set(models.Model):
    name = models.TextField(null=False)
    category = models.ForeignKey('Category')
    description = models.TextField(null=False, blank=True)
    big_img_url = models.TextField(null=False, blank=True)
    small_img_url = models.TextField(null=False, blank=True)
    discount_difference = models.IntegerField(null=False, default=0)

    is_active = models.BooleanField(default=True)

    def __unicode__(self):
        return '(%r)Set : name(%s)' \
               % (self.id, self.name)

    def __str__(self):
        return unicode(self).encode('utf-8')

class Tag(models.Model):
    name = models.TextField(unique=True)

    def __unicode__(self):
        return '(%r)Tags : name(%s)' \
               % (self.id, self.name)

    def __str__(self):
        return unicode(self).encode('utf-8')

class SetTag(models.Model):
    set = models.ForeignKey('Set')
    tag = models.ForeignKey('Tag')

class SetProduct(models.Model):
    set = models.ForeignKey('Set')
    product = models.ForeignKey('Product')
    created = models.DateTimeField(auto_now_add=True, default=datetime.now)

    def __unicode__(self):
        return '(%r)SetProduct : set(%s) product(%s)' \
               % (self.id, self.set.name, self.product.name)

    def __str__(self):
        return unicode(self).encode('utf-8')

class ChangeableProduct(models.Model):
    set = models.ForeignKey('Set')
    product = models.ForeignKey('Product')

    class Meta:
        unique_together = (
            ("set", "product"))

    def __unicode__(self):
        return '(%r)ChangeableProduct : set(%s) product(%s)' \
               % (self.id, self.set.name, self.product.name)

    def __str__(self):
        return unicode(self).encode('utf-8')

class ChangeableProductInfo(models.Model):
    changeable_product = models.ForeignKey('ChangeableProduct')
    product = models.ForeignKey('Product')

    class Meta:
        unique_together = (
            ("changeable_product", "product"))

    def __unicode__(self):
        return '(%r)ChangeableProductInfo : changeable_product(%r) product(%s)' \
               % (self.id, self.changeable_product, self.product.name)

    def __str__(self):
        return unicode(self).encode('utf-8')


class BlogReview(models.Model):
    product = models.ForeignKey('Product')
    writer = models.TextField(null=False, blank=True)
    url = models.TextField(null=False, blank=True)
    big_img_url = models.TextField(null=False, blank=True)
    small_img_url = models.TextField(null=False, blank=True)
    review_created_time = models.DateTimeField(default=datetime.now)
    summary = models.TextField(null=False, blank=True)
    created = models.DateTimeField(auto_now_add=True, default=datetime.now)