from django.contrib import admin
from common.models import NProduct, ProductDetail, ProductAnalysis, ProductAnalysisDetail, NCategory


admin.site.register(NCategory)

class NProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'brand', 'category', 'price', 'capacity', 'capacity_unit', 'thumbnail')
    list_editable = ['thumbnail']

admin.site.register(NProduct, NProductAdmin)

class ProductDetailAdmin(admin.ModelAdmin):
    list_display = ('product', 'function', 'estimation_period')

admin.site.register(ProductDetail, ProductDetailAdmin)

class ProductAnalysisAdmin(admin.ModelAdmin):
    list_display = ('product', 'total_count', 'skin_type', 'feature')

admin.site.register(ProductAnalysis, ProductAnalysisAdmin)

class ProductAnalysisDetailAdmin(admin.ModelAdmin):
    list_display = ('id', 'content', 'count', 'type')

admin.site.register(ProductAnalysisDetail, ProductAnalysisDetailAdmin)
