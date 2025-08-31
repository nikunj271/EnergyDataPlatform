from django.contrib import admin
from .models import Product, MarketData

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

@admin.register(MarketData)
class MarketDataAdmin(admin.ModelAdmin):
    list_display = ('product', 'date', 'interval', 'purchase_bid', 'sell_bid', 'mcp', 'mcv')
    list_filter = ('product', 'date')
    search_fields = ('product__name',)
