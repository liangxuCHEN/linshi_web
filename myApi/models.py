from django.db import models


class Userate(models.Model):
    name = models.CharField(max_length = 40)
    rate = models.FloatField()
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('created',)