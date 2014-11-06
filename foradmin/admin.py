from django.contrib import admin
from foradmin.models import SurveyItem, SurveyItemOption
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

class SurveyItemAdmin(admin.ModelAdmin):
    list_display = ('question','type')
    list_editable = ('type',)
    list_display_links = ('question',)
admin.site.register(SurveyItem, SurveyItemAdmin)

class SurveyItemOptionAdmin(admin.ModelAdmin):
    list_display = ('item','content')
    list_editable = ('content',)
    list_display_links = ('item',)
admin.site.register(SurveyItemOption, SurveyItemOptionAdmin)