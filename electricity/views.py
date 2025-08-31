from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import render
from django.db.models import Avg, Sum
from .models import Product, MarketData
from .serializers import ProductSerializer, MarketDataSerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class MarketDataViewSet(viewsets.ModelViewSet):
    queryset = MarketData.objects.all()
    serializer_class = MarketDataSerializer

@api_view(['GET'])
def market_summary(request):
    product = request.GET.get('product', 'DAM')
    start = request.GET.get('start')
    end = request.GET.get('end')

    data = MarketData.objects.filter(product__name=product, date__range=[start, end])
    weighted_sum = sum([d.mcp * d.mcv for d in data])
    total_volume = sum([d.mcv for d in data])
    weighted_avg_mcp = weighted_sum / total_volume if total_volume else 0

    return Response({
        "product": product,
        "start": start,
        "end": end,
        "weighted_avg_mcp": round(weighted_avg_mcp, 2),
        "total_volume": round(total_volume, 2)
    })

def dashboard(request):
    stats = MarketData.objects.values('product__name', 'date').annotate(
        avg_price=Avg('mcp'), total_volume=Sum('mcv')
    ).order_by('-date')[:10]
    return render(request, 'electricity/dashboard.html', {'stats': stats})
