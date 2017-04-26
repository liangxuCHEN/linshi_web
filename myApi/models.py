from django.db import models


class UseRate(models.Model):
    name = models.TextField()
    rate = models.FloatField()
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('created',)


