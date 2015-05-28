# coding: utf-8
# django import_export 구현을 위한 Resource 정의 파일
__author__ = 'woongkaa'

from import_export import resources
from models import NCategory, NProduct


class CategoryResource(resources.ModelResource):

    class Meta:
        model = NCategory
        fields = ('id', 'name', 'name_for_kor',)


class ProductResource(resources.ModelResource):

    class Meta:
        model = NProduct
        fields = ('name', 'brand', 'price', 'capacity', 'capacity_unit', 'category__name_for_kor', 'category',)