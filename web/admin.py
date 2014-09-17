from django.contrib import admin
from .models import Category, Product, ProductDescriptionImage, ProductImage, Set, SetProduct, ChangeableProduct, \
    ChangeableProductInfo, BlogReview, Brand, Magazine, ProductMagazine, Tag, SetTag, Faq
from web.models import SetDescriptionImage


class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category', 'original_price', 'discount_price', 'fit_skin_type', 'thumbnail_image', 'video_url', 'brand', 'brandname', 'maker', 'country', 'capacity', 'description', 'short_desc', 'use_expired_date', 'production_date', 'usage', 'ingredient', 'judge_result', 'precautions', 'quality_guarantee_standard')
    list_editable = ('category', 'original_price', 'discount_price', 'fit_skin_type', 'thumbnail_image', 'video_url', 'brand', 'brandname', 'maker', 'country', 'capacity', 'description', 'short_desc', 'use_expired_date', 'production_date', 'usage', 'ingredient', 'judge_result', 'precautions', 'quality_guarantee_standard')
    list_display_links = ('name',)

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

class MagazineAdmin(admin.ModelAdmin):
    list_display = ('title',)
    # list_editable = ('title',)
    list_display_links = ('title',)

admin.site.register(Magazine, MagazineAdmin)

class ProductMagazineAdmin(admin.ModelAdmin):
    list_display = ('product', 'magazine', 'year', 'month', 'title', 'author', 'link')
    list_editable = ('year', 'month', 'title', 'author', 'link',)
    list_display_links = ('product', 'magazine')

admin.site.register(ProductMagazine, ProductMagazineAdmin)

class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)
    # list_editable = ('name',)
    # list_display_links = ()

admin.site.register(Tag, TagAdmin)

class SetTagAdmin(admin.ModelAdmin):
    list_display = ('set', 'tag')
    # list_editable = ('year', 'month', 'link',)
    list_display_links = ('set', 'tag')

admin.site.register(SetTag, SetTagAdmin)

class FaqAdmin(admin.ModelAdmin):
    list_display = ('title', 'content', 'is_active', 'created')
    list_editable = ('content', 'is_active',)
    # list_display_links = ()
admin.site.register(Faq, FaqAdmin)

class SetDescriptionImageAdmin(admin.ModelAdmin):
    list_display = ('set', 'image')
    list_editable = ('image',)
    list_display_links = ('set', )
admin.site.register(SetDescriptionImage, SetDescriptionImageAdmin)

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_set', 'big_image', 'small_image')
    list_editable = ('is_set', 'big_image', 'small_image',)
    # list_display_links = ()
admin.site.register(Category, CategoryAdmin)

class SetAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'description', 'big_img', 'small_img', 'discount_difference', 'is_active' )
    list_editable = ('description', 'big_img', 'small_img', 'discount_difference', 'is_active',)
    list_display_links = ('name', 'category',)
admin.site.register(Set, SetAdmin)

admin.site.register(ProductDescriptionImage)
admin.site.register(ProductImage)
admin.site.register(SetProduct)
admin.site.register(ChangeableProduct)
admin.site.register(ChangeableProductInfo)