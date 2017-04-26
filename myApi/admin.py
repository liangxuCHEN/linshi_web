from django.contrib import admin
from myApi.models import Userate


class UseRateAdmin(admin.ModelAdmin):
    list_display = ('created', 'name', 'rate')

admin.site.register(Userate, UseRateAdmin)
