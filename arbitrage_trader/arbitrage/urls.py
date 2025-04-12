from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ExchangeConfigViewSet, ArbitrageOpportunityViewSet, ConfigurationViewSet

router = DefaultRouter()
router.register(r'exchanges', ExchangeConfigViewSet)
router.register(r'opportunities', ArbitrageOpportunityViewSet)
router.register(r'config', ConfigurationViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
