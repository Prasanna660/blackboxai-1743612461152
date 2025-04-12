import time
import ccxt
from django.core.management.base import BaseCommand
from django.db import transaction
from arbitrage.models import ExchangeConfig, ArbitrageOpportunity, Configuration

class Command(BaseCommand):
    help = 'Runs the arbitrage detection bot'

    def handle(self, *args, **options):
        self.stdout.write("Starting arbitrage bot...")
        
        while True:
            try:
                config = Configuration.objects.first()
                if not config:
                    config = Configuration.objects.create()
                    self.stdout.write("Created default configuration")

                if not config.active:
                    time.sleep(10)
                    continue

                # Initialize exchanges with robust error handling
                exchange_configs = [
                    ('kucoin', ccxt.kucoin),
                    ('okx', ccxt.okx),
                    ('gateio', ccxt.gateio)
                ]
                
                exchanges = {}
                for name, exchange_class in exchange_configs:
                    try:
                        exchange = exchange_class({
                            'enableRateLimit': True,
                            'timeout': 10000
                        })
                        exchange.load_markets()  # Test connection
                        exchanges[name] = exchange
                        self.stdout.write(f"Successfully connected to {name}")
                    except Exception as e:
                        self.stdout.write(f"Error initializing {name}: {str(e)}")
                        continue

                if len(exchanges) < 2:
                    self.stdout.write("Need at least 2 exchanges to find arbitrage")
                    time.sleep(10)
                    continue

                # Fetch prices with improved error handling
                prices = {}
                for name, exchange in exchanges.items():
                    try:
                        order_book = exchange.fetch_order_book(config.symbol)
                        if order_book['bids'] and order_book['asks']:
                            prices[name] = {
                                'bid': order_book['bids'][0][0],
                                'ask': order_book['asks'][0][0]
                            }
                    except Exception as e:
                        self.stdout.write(f"Error fetching prices from {name}: {str(e)}")

                # Find arbitrage opportunities
                if len(prices) >= 2:
                    min_ask = min(prices.items(), key=lambda x: x[1]['ask'])
                    max_bid = max(prices.items(), key=lambda x: x[1]['bid'])
                    profit = max_bid[1]['bid'] - min_ask[1]['ask']

                    if profit > config.profit_threshold:
                        with transaction.atomic():
                            ArbitrageOpportunity.objects.create(
                                buy_exchange=min_ask[0],
                                sell_exchange=max_bid[0],
                                buy_price=min_ask[1]['ask'],
                                sell_price=max_bid[1]['bid'],
                                profit=profit
                            )
                        self.stdout.write(f"Arbitrage opportunity found! Profit: ${profit:.2f}")

            except Exception as e:
                self.stdout.write(f"Bot error: {str(e)}")
                time.sleep(10)

            time.sleep(5)