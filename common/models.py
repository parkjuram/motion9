#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.db import models
from django.utils.encoding import python_2_unicode_compatible


# prefix 'N' in class name means renewal version model(2015/01/07)
@python_2_unicode_compatible
class NCategory(models.Model):
    name = models.CharField(max_length=20, unique=True)
    name_for_kor = models.CharField(max_length=20, default='')
    order = models.SmallIntegerField(null=False, default=1)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class NProduct(models.Model):
    name = models.CharField(max_length=40, null=False)
    brand = models.CharField(max_length=20, null=False, blank=True)
    category = models.ForeignKey(NCategory)
    price = models.IntegerField(null=False, default=0)
    capacity = models.IntegerField(null=False, default=0)
    capacity_unit = models.CharField(max_length=10, null=False, default='ml')
    thumbnail = models.ImageField(null=True, upload_to='thumbnail/product/', blank=True)

    # class Meta:
    # ordering = ['-category']

    @property
    def thumbnail_url(self):
        if self.thumbnail and hasattr(self.thumbnail, 'url'):
            return self.thumbnail.url
        else:
            return '#'

    @property
    def unit_price(self):
        return self.price / self.capacity

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class ProductDetail(models.Model):
    product = models.OneToOneField(NProduct)
    function = models.TextField(null=False, blank=True)
    estimation_period = models.SmallIntegerField(null=False, default=0)

    def __str__(self):
        return self.product.name


@python_2_unicode_compatible
class ProductAnalysis(models.Model):
    product = models.OneToOneField(NProduct)
    total_count = models.IntegerField(null=False, default=0)
    skin_type = models.CharField(max_length=4, null=False,
                                 blank=True)  # one start character of ('dry', 'oily', 'neutral', 'complex')
    feature = models.CharField(max_length=2, null=False,
                               default='no')  # two start character of ('whitening', 'wrinkle', 'trouble', 'nothing')
    general_review = models.TextField(null=False, blank=True)

    @property
    def skin_type_for_display(self):
        str = ""
        if 'd' in self.skin_type:
            str += "[건성]"
        if 'o' in self.skin_type:
            str += "[지성]"
        if 'n' in self.skin_type:
            str += "[중성]"
        if 'c' in self.skin_type:
            str += "[복합성]"

        return str

    @property
    def feature_for_display(self):
        str = ""
        if 'wh' in self.feature:
            str += "[미백]"
        if 'wr' in self.feature:
            str += "[주름개선]"
        if 'su' in self.feature:
            str += "[자외선차단]"

        if len(str) == 0:
            str = '[해당사항 없음]'

        return str


    def __str__(self):
        return unicode(self.product)


@python_2_unicode_compatible
class ProductAnalysisDetail(models.Model):
    product_analysis = models.ForeignKey(ProductAnalysis, related_name='details')
    content = models.TextField(null=False, blank=True)
    count = models.IntegerField(null=False, default=0)
    type = models.CharField(max_length=20, null=False)

    def __str__(self):
        return unicode(self.product_analysis)

    class Meta:
        unique_together = (("product_analysis", "content"),)
        ordering = ['-count']