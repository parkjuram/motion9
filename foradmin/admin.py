from django.contrib import admin
from .models import MainImage, Advertisement, Preference


class MainImageAdmin(admin.ModelAdmin):
    list_display = ('name', 'image')
admin.site.register(MainImage, MainImageAdmin)

class AdvertisementAdmin(admin.ModelAdmin):
    list_display = ( 'title', 'category', 'image', 'mobile_image')
    list_editable = ( 'image', 'mobile_image', )
    list_display_links = ( 'title', 'category',)

admin.site.register(Advertisement, AdvertisementAdmin)

class PreferenceAdmin(admin.ModelAdmin):
    list_display = ('name','content')
    list_editable = ('content',)
    list_display_links = ('name',)
admin.site.register(Preference, PreferenceAdmin)
