from django.contrib import admin

from geolocation.models import *
from geolocation.forms import ShopEntryForm

class ShopAdmin(admin.ModelAdmin):
    form = ShopEntryForm
    list_display = ('name', 'location',)


admin.site.register(Shop, ShopAdmin)


