from rest_framework import serializers
from .models import ExchangeConfig, ArbitrageOpportunity, Configuration

class ExchangeConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExchangeConfig
        fields = '__all__'

class ArbitrageOpportunitySerializer(serializers.ModelSerializer):
    class Meta:
        model = ArbitrageOpportunity
        fields = '__all__'

class ConfigurationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Configuration
        fields = '__all__'