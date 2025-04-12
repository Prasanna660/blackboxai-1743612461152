from django.contrib import admin
from .models import ExchangeConfig, ArbitrageOpportunity, Configuration

@admin.register(ExchangeConfig)
class ExchangeConfigAdmin(admin.ModelAdmin):
    list_display = ('name',)
    fields = ('name', 'api_key', 'secret')
    search_fields = ('name',)

@admin.register(ArbitrageOpportunity)
class ArbitrageOpportunityAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'buy_exchange', 'sell_exchange', 'profit')
    list_filter = ('buy_exchange', 'sell_exchange')
    readonly_fields = ('timestamp',)
    date_hierarchy = 'timestamp'

@admin.register(Configuration)
class ConfigurationAdmin(admin.ModelAdmin):
    list_display = ('active', 'profit_threshold', 'trade_amount', 'symbol')
    fields = ('active', 'profit_threshold', 'trade_amount', 'symbol')
