from django.contrib import admin
from common.models import NProduct


class NProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'brand', 'price', 'capacity')
    # list_display_links = ()
admin.site.register(NProduct, NProductAdmin)