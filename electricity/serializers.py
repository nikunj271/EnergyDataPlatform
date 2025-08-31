from rest_framework import serializers
from .models import Product, MarketData

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class MarketDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = MarketData
        fields = '__all__'
