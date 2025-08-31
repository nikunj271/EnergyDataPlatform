from django.db import models

PRODUCT_CHOICES = (
    ('DAM', 'Day Ahead Market'),
    ('RTM', 'Real Time Market'),
)

class Product(models.Model):
    name = models.CharField(max_length=10, choices=PRODUCT_CHOICES, unique=True)
    def __str__(self):
        return self.get_name_display()

class MarketData(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    date = models.DateField()
    interval = models.PositiveIntegerField()
    purchase_bid = models.FloatField()
    sell_bid = models.FloatField()
    mcp = models.FloatField()
    mcv = models.FloatField()

    class Meta:
        unique_together = ('product', 'date', 'interval')
        ordering = ['date', 'interval']

    def __str__(self):
        return f"{self.product} | {self.date} | Interval {self.interval}"
