from django.contrib import admin
from myApi.models import Userate


class UseRateAdmin(admin.ModelAdmin):
    list_display = ('created', 'rate', 'name')

admin.site.register(Userate, UseRateAdmin)
