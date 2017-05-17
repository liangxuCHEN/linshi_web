from django.contrib import admin
from myApi.models import Userate, ProductRateDetail, Project


class UseRateAdmin(admin.ModelAdmin):
    list_display = ('created', 'rate', 'name')


class ProductRateDetailAdmin(admin.ModelAdmin):
    list_display = ('sheet_name', 'avg_rate')


class ProjectAdmin(admin.ModelAdmin):
    list_display = ('created', 'comment')

admin.site.register(Userate, UseRateAdmin)
admin.site.register(ProductRateDetail, ProductRateDetailAdmin)
admin.site.register(Project, ProjectAdmin)
