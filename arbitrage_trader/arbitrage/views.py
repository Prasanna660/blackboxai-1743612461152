from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import ExchangeConfig, ArbitrageOpportunity, Configuration
from .serializers import ExchangeConfigSerializer, ArbitrageOpportunitySerializer, ConfigurationSerializer

class ExchangeConfigViewSet(viewsets.ModelViewSet):
    queryset = ExchangeConfig.objects.all()
    serializer_class = ExchangeConfigSerializer

class ArbitrageOpportunityViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ArbitrageOpportunity.objects.all().order_by('-timestamp')
    serializer_class = ArbitrageOpportunitySerializer
    pagination_class = None

class ConfigurationViewSet(viewsets.ModelViewSet):
    queryset = Configuration.objects.all()
    serializer_class = ConfigurationSerializer

    @action(detail=False, methods=['post'])
    def toggle_bot(self, request):
        config = Configuration.objects.first()
        config.active = not config.active
        config.save()
        return Response({'status': 'success', 'active': config.active})
