from django.db import models


class Userate(models.Model):
    name = models.CharField(max_length=40)
    rate = models.FloatField()
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('created',)


class ProductRateDetail(models.Model):
    sheet_name = models.CharField(max_length=40)
    num_sheet = models.IntegerField()
    avg_rate = models.FloatField()
    rates = models.CharField(max_length=256)
    detail = models.TextField()
    num_shape = models.CharField(max_length=512)
    sheet_num_shape = models.CharField(max_length=512)
