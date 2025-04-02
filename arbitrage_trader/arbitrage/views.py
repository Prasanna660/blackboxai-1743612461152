from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import ArbitrageOpportunity, Configuration

def dashboard(request):
    config = Configuration.objects.first() or Configuration.objects.create()
    opportunities = ArbitrageOpportunity.objects.all()[:20]
    return render(request, 'arbitrage/dashboard.html', {
        'config': config,
        'opportunities': opportunities
    })

def get_opportunities(request):
    opportunities = list(ArbitrageOpportunity.objects.order_by('-timestamp')[:10].values(
        'timestamp', 'buy_exchange', 'sell_exchange', 'buy_price', 'sell_price', 'profit'
    ))
    return JsonResponse(opportunities, safe=False)

@require_POST
def update_config(request):
    config = Configuration.objects.first() or Configuration.objects.create()
    config.profit_threshold = float(request.POST.get('profit_threshold', 10))
    config.trade_amount = float(request.POST.get('trade_amount', 0.01))
    config.symbol = request.POST.get('symbol', 'BTC/USDT')
    config.save()
    return redirect('dashboard')

@require_POST
def toggle_bot(request):
    config = Configuration.objects.first() or Configuration.objects.create()
    config.active = not config.active
    config.save()
    return JsonResponse({'active': config.active})
