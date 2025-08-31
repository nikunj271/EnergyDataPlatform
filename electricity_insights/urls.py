from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from electricity.views import ProductViewSet, MarketDataViewSet, market_summary, dashboard

router = routers.DefaultRouter()
router.register(r'products', ProductViewSet)
router.register(r'marketdata', MarketDataViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/summary/', market_summary),
    path('', dashboard),
]
