# coding: utf-8
__author__ = 'woongkaa'

from import_export import resources
from models import Product


class ProductResource(resources.ModelResource):
    class Meta:
        model = Product
        fields = ('id', 'name', 'category__name', 'brand__name_kor', 'original_price', 'maker', 'fit_skin_type',
                  'usage', 'ingredient', 'precautions', 'quality_guarantee_standard', 'description', )