from django.contrib import admin
from .models import MainImage, Advertisement


class MainImageAdmin(admin.ModelAdmin):
    list_display = ('name', 'image')
admin.site.register(MainImage, MainImageAdmin)

class AdvertisementAdmin(admin.ModelAdmin):
    list_display = ( 'type', 'image', 'link')
    list_editable = ('image', 'link')

admin.site.register(Advertisement, AdvertisementAdmin)
