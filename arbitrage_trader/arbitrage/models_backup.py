from django.db import models
from django.utils import timezone

class ExchangeConfig(models.Model):
    name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return self.name

class ArbitrageOpportunity(models.Model):
    exchange1 = models.CharField(max_length=50)
    exchange2 = models.CharField(max_length=50)
    symbol = models.CharField(max_length=20)
    price_diff = models.DecimalField(max_digits=20, decimal_places=8)
    profit = models.DecimalField(max_digits=20, decimal_places=2)
    timestamp = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['timestamp']),
            models.Index(fields=['symbol']),
        ]

    def __str__(self):
        return f"{self.symbol} {self.exchange1}-{self.exchange2} ${self.profit:.2f}"
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']
        verbose_name_plural = 'Arbitrage Opportunities'

    def __str__(self):
        return f"{self.buy_exchange} → {self.sell_exchange} (${self.profit:.2f})"

class Configuration(models.Model):
    profit_threshold = models.DecimalField(max_digits=10, decimal_places=2, default=10)
    trade_amount = models.DecimalField(max_digits=10, decimal_places=6, default=0.01)
    active = models.BooleanField(default=False)
    symbol = models.CharField(max_length=10, default='BTC/USDT')

    def __str__(self):
        return f"Config (Active: {self.active})"
