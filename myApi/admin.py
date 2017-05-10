from django.contrib import admin
from myApi.models import Userate, ProductRateDetail


class UseRateAdmin(admin.ModelAdmin):
    list_display = ('created', 'rate', 'name')


class ProductRateDetailAdmin(admin.ModelAdmin):
    list_display = ('sheet_name', 'avg_rate')

admin.site.register(Userate, UseRateAdmin)
admin.site.register(ProductRateDetail, ProductRateDetailAdmin)
