from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Sum

from .tables import TransactionTable, AccountTable, OrderbookTable
from .models import Transaction, Account, TransactionType
from .forms import AccountForm, ProfitAndLossForm, ChoiceExchangeForm

import requests
import json
from operator import itemgetter


def transaction_view(request):
    if request.user.is_authenticated:
        queryset = Transaction.objects.filter(customer=request.user)
        table = TransactionTable(queryset)
        table.paginate(page=request.GET.get('page', 1), per_page=10)
        return render(request, 'exchange/transactions.html', {'table': table})
    else:
        return HttpResponse('Please login first...')


def exchange_account_view(request):
    if not request.user.is_authenticated:
        return HttpResponse('Please login first...')
    else:
        queryset = Account.objects.filter(owner=request.user)
        table = AccountTable(queryset)
        table.paginate(page=request.GET.get('page', 1), per_page=10)
        if request.method == 'POST':
            form = AccountForm(request.POST)
            if form.is_valid():
                account = Account.objects.create(
                    user=request.user,
                    exchange=form.cleaned_data['exchange'],
                    exchange_email=form.cleaned_data['exchange_email'],
                    exchange_password=form.cleaned_data['exchange_password'],
                    exchange_phone_number=form.cleaned_data['exchange_phone_number']
                )
        else:
            form = AccountForm()
        return render(request, 'exchange/account.html', {'form': form,
                                                         'table': table})


def profitandloss_view(request):
    if not request.user.is_authenticated:
        return HttpResponse('Please login first...')
    if request.method == 'POST':
        form = ProfitAndLossForm(request.POST)
        if form.is_valid():
            if not form.cleaned_data['ranged_show']:
                queryset = Transaction.objects.filter(customer=request.user)
            else:
                queryset = Transaction.objects.filter(customer=request.user,
                                                      completion_date__gte=form.cleaned_data['range_start'],
                                                      completion_date__lte=form.cleaned_data['range_end'])
            table = TransactionTable(queryset)
            table.paginate(page=request.GET.get('page', 1), per_page=10)
            # celery task below
            sell_sum = queryset.filter(type=TransactionType.SELL).aggregate(sell_sum=Sum('price'))['sell_sum']
            buy_sum = queryset.filter(type=TransactionType.BUY).aggregate(buy_sum=Sum('price'))['buy_sum']
            # abow sums could be calculated by opposite transactions
            if not sell_sum:
                sell_sum = 0
            if not buy_sum:
                buy_sum = 0
            final = int(sell_sum) - int(buy_sum)
            return render(request, 'exchange/profitandloss.html', {'form': form,
                                                                   'table': table,
                                                                   'final': final})
    else:
        form = ProfitAndLossForm()
        return render(request, 'exchange/profitandloss.html', {'form': form,
                                                               'final': 'Please specify range to Calculate Profit and Loss'})


def orderbooks_view(request):
    if not request.user.is_authenticated:
        return HttpResponse('Please login first...')
    if request.method == 'POST':
        form = ChoiceExchangeForm(request.POST)
        if form.is_valid():
            coin = form.cleaned_data['currency']
            nobitex_orderbook = json.loads(
                requests.get('https://api.nobitex.ir/v2/orderbook/' + str(coin).upper() + 'IRT').text)
            wallex_orderbook = json.loads(
                requests.get('https://api.wallex.ir/v1/depth?symbol=' + str(coin).upper() + 'TMN').text)
            phinix_orderbook = json.loads(
                requests.get('https://api.phinix.ir/v1/depth?symbol=' + str(coin).upper() + 'TMN').text)
            nobitex_bids = nobitex_orderbook['bids'][:5]
            nobitex_asks = nobitex_orderbook['asks'][:5]
            wallex_bids = wallex_orderbook['result']['bid'][:5]
            wallex_asks = wallex_orderbook['result']['ask'][:5]
            phinix_bids = phinix_orderbook['result']['bid'][:5]
            phinix_asks = phinix_orderbook['result']['ask'][:5]
            nobitex_bids = [{'price': float(bid[0]), 'quantity': float(bid[1]), 'exchange': 'Nobitex'} for bid in nobitex_bids]
            nobitex_asks = [{'price': float(ask[0]), 'quantity': float(ask[1]), 'exchange': 'Nobitex'} for ask in nobitex_asks]
            wallex_bids = [{'price': float(bid['price']), 'quantity': float(bid['quantity']), 'exchange': 'Wallex'} for bid in wallex_bids]
            wallex_asks = [{'price': float(ask['price']), 'quantity': float(ask['quantity']), 'exchange': 'Wallex'} for ask in wallex_asks]
            phinix_bids = [{'price': float(bid['price']), 'quantity': float(bid['quantity']), 'exchange': 'Phinix'} for bid in phinix_bids]
            phinix_asks = [{'price': float(ask['price']), 'quantity': float(ask['quantity']), 'exchange': 'Phinix'} for ask in phinix_asks]
            bids = (nobitex_bids + wallex_bids + phinix_bids)
            asks = (nobitex_asks + wallex_asks + phinix_asks)
            bids = sorted(bids, key=itemgetter('price'))[::-1][:8]
            asks = sorted(asks, key=itemgetter('price'))[:8]
            bids_table = OrderbookTable(bids)
            asks_table = OrderbookTable(asks)
            return render(request, 'exchange/orderbooks.html', {'form': form,
                                                                'bids_table': bids_table,
                                                                'asks_table': asks_table, })
    else:
        form = ChoiceExchangeForm()
        return render(request, 'exchange/orderbooks.html', {'form': form})
