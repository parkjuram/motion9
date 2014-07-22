from django.contrib import admin
from .models import Category, Product, ProductDescriptionImage, ProductImage, Set, SetProduct, ChangeableProduct, \
    ChangeableProductInfo, BlogReview, Brand

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'original_price', 'discount_price', 'fit_skin_type', 'thumbnail_image', 'video_url', 'brand', 'brandname', 'maker', 'country', 'capacity', 'description', 'short_desc', 'use_expired_date', 'production_date', 'usage', 'ingredient', 'judge_result', 'precautions', 'quality_guarantee_standard')
    list_editable = ('category', 'original_price', 'discount_price', 'fit_skin_type', 'thumbnail_image', 'video_url', 'brand', 'brandname', 'maker', 'country', 'capacity', 'description', 'short_desc', 'use_expired_date', 'production_date', 'usage', 'ingredient', 'judge_result', 'precautions', 'quality_guarantee_standard')
    list_display_links = ('name',)

# name = models.TextField(unique=True)
#     category = models.ForeignKey(Category)
#
#     original_price = models.IntegerField(null=False, default=0)
#     discount_price = models.IntegerField(null=False, default=0)
#     fit_skin_type = models.CharField(max_length=30, blank=True)
#
#     thumbnail_image = models.ImageField(null=True, upload_to='product/')
#     video_url = models.URLField(blank=True)
#     brand = models.ForeignKey(Brand)
#     brandname = models.CharField(max_length=30, blank=True)
#     maker = models.CharField(max_length=30, blank=True)
#     country = models.CharField(max_length=30, blank=True)
#     capacity = models.CharField(max_length=10, blank=True)
#     description = models.TextField(blank=True)
#     short_desc = models.CharField(max_length=100, blank=True)
#     use_expired_date = models.CharField(max_length=50, blank=True)
#     production_date = models.CharField(max_length=50, blank=True)
#     usage = models.TextField(blank=True)
#     ingredient = models.TextField(blank=True)
#     judge_result = models.CharField(max_length=100, blank=True)
#     precautions = models.TextField(blank=True)
#     quality_guarantee_standard = models.CharField(max_length=100, blank=True)

admin.site.register(Product, ProductAdmin)


class BrandAdmin(admin.ModelAdmin):
    list_display = ('name_eng', 'name_kor', 'is_repr_to_eng', 'is_domestic')
    list_editable = ('name_kor', 'is_repr_to_eng', 'is_domestic',)
    # list_display_links = ('name_kor', 'is_repr_to_eng')
    list_filter = ('name_eng', 'name_kor', 'is_repr_to_eng', 'is_domestic')

admin.site.register(Brand, BrandAdmin)


class BlogReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'writer', 'url', 'big_img_url', 'small_img_url', 'review_created_time', 'summary')
    list_editable = ('writer', 'url', 'big_img_url', 'small_img_url', 'review_created_time', 'summary')
    list_display_links = ('product',)
    # list_filter = ('product', 'writer', 'url', 'big_img_url', 'small_img_url', 'review_created_time', 'summary')

admin.site.register(BlogReview, BlogReviewAdmin)



admin.site.register(Category)

admin.site.register(ProductDescriptionImage)
admin.site.register(ProductImage)
admin.site.register(Set)
admin.site.register(SetProduct)
admin.site.register(ChangeableProduct)
admin.site.register(ChangeableProductInfo)