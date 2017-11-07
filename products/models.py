from django.db import models
from orgs.models import Org
from django.utils import timezone


class Product(models.Model):
    name = models.CharField(max_length=200)
    org = models.ForeignKey(Org, on_delete=models.CASCADE, default=0, related_name='products')
    description = models.TextField()
    order_price = models.DecimalField(max_digits=8, decimal_places=2)
    sell_price = models.DecimalField(max_digits=8, decimal_places=2)
    created_date = models.DateTimeField(
            default=timezone.now)
    published_date = models.DateTimeField(
            blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.name
