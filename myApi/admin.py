from django.contrib import admin
from myApi.models import UseRate


class UseRateAdmin(admin.ModelAdmin):
    list_display = ('created', 'name', 'rate')

admin.site.register(UseRate, UseRateAdmin)
