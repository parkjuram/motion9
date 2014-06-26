from django.contrib import admin
from .models import Category, Product, ProductDescriptionImage, ProductImage, Set, SetProduct, ChangeableProduct, \
    ChangeableProductInfo, BlogReview

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(ProductDescriptionImage)
admin.site.register(ProductImage)
admin.site.register(Set)
admin.site.register(SetProduct)
admin.site.register(ChangeableProduct)
admin.site.register(ChangeableProductInfo)
admin.site.register(BlogReview)

