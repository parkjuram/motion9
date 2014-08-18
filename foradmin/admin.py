from django.contrib import admin
from .models import MainImage

class MainImageAdmin(admin.ModelAdmin):
    list_display = ('name', 'image')

admin.site.register(MainImage, MainImageAdmin)