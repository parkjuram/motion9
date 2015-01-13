from django.contrib import admin
from common.models import NProduct, ProductDetail, ProductAnalysis, ProductAnalysisDetail


class NProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'brand', 'price', 'capacity')

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




class NSurveyAdmin(admin.ModelAdmin):
    list_display = ('id', 'content', 'count', 'type')

admin.site.register(NSurvey, ProductAnalysisDetailAdmin)

class NUserSurveyAdmin(admin.ModelAdmin):
    list_display = ('id', 'content', 'count', 'type')

admin.site.register(NUserSurvey, ProductAnalysisDetailAdmin)

class SurveyResultAdmin(admin.ModelAdmin):
    list_display = ('id', 'content', 'count', 'type')

admin.site.register(SurveyResult, ProductAnalysisDetailAdmin)