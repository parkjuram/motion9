from django.contrib import admin
from .models import Category, Product, ProductDescriptionImage, ProductImage, Set, SetProduct, ChangeableProduct, \
    ChangeableProductInfo, BlogReview, Brand


class BrandAdmin(admin.ModelAdmin):
    list_display = ('name_eng', 'name_kor', 'is_repr_to_eng', 'is_domestic')
    list_editable = ('name_kor', 'is_repr_to_eng', 'is_domestic',)
    # list_display_links = ('name_kor', 'is_repr_to_eng')
    list_filter = ('name_eng', 'name_kor', 'is_repr_to_eng', 'is_domestic')

class BlogReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'writer', 'url', 'big_img_url', 'small_img_url', 'review_created_time', 'summary')
    list_editable = ('writer', 'url', 'big_img_url', 'small_img_url', 'review_created_time', 'summary')
    list_display_links = ('product',)
    # list_filter = ('product', 'writer', 'url', 'big_img_url', 'small_img_url', 'review_created_time', 'summary')

admin.site.register(Brand, BrandAdmin)
admin.site.register(BlogReview, BlogReviewAdmin)

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(ProductDescriptionImage)
admin.site.register(ProductImage)
admin.site.register(Set)
admin.site.register(SetProduct)
admin.site.register(ChangeableProduct)
admin.site.register(ChangeableProductInfo)
