from django.contrib import admin
from common.models import NProduct, ProductDetail, ProductAnalysis, ProductAnalysisDetail, NCategory
from import_export.admin import ImportExportMixin
from resources import *


admin.site.register(NCategory)


class NProductAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ('name', 'brand', 'category', 'price', 'capacity', 'capacity_unit', 'thumbnail')
    list_editable = ['thumbnail']
    resource_class = ProductResource

admin.site.register(NProduct, NProductAdmin)


class ProductDetailAdmin(admin.ModelAdmin):
    list_display = ('product', 'function', 'estimation_period')

admin.site.register(ProductDetail, ProductDetailAdmin)


class ProductAnalysisAdmin(admin.ModelAdmin):
    list_display = ('product', 'total_count', 'skin_type', 'feature')

admin.site.register(ProductAnalysis, ProductAnalysisAdmin)


class ProductAnalysisDetailAdmin(admin.ModelAdmin):
    list_display = ('product_analysis', 'content', 'count', 'type')
    list_filter = ['product_analysis']

admin.site.register(ProductAnalysisDetail, ProductAnalysisDetailAdmin)
