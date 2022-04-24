from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Sum
from django.core.cache import cache


from .tables import TransactionTable, AccountTable, AsksTable, BidsTable
from .models import Transaction, Account, TransactionType, Status
from .forms import AccountForm, ProfitAndLossForm, ChoiceExchangeForm

import requests
import json


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
                    owner=request.user,
                    exchange=form.cleaned_data['exchange'],
                    exchange_email=form.cleaned_data['exchange_email'],
                    exchange_password=form.cleaned_data['exchange_password'],
                    exchange_phone_number=form.cleaned_data['exchange_phone_number'],
                    token=form.cleaned_data['token'],
                    wallet_address=form.cleaned_data['wallet_address']
                )
        else:
            form = AccountForm()
        return render(request, 'exchange/account.html', {'form': form,
                                                         'table': table})


def account_edit_view(request, pk):
    account = Account.objects.get(pk=pk)
    user = request.user
    if request.method == "POST":
        form = AccountForm(request.POST)
        if form.is_valid():
            account.token = form.cleaned_data['token']
            account.wallet_address = form.cleaned_data['wallet_address']
            account.save()
    else:
        form = AccountForm(initial={
            'exchange': account.exchange,
            'exchange_email': account.exchange_email,
            'exchange_phone_number': account.exchange_phone_number,
            'exchange_password': account.exchange_password
        })
    return render(request, 'exchange/edit_account.html', {'form': form})


def profitandloss_view(request):
    if not request.user.is_authenticated:
        return HttpResponse('Please login first...')
    if request.method == 'POST':
        form = ProfitAndLossForm(request.POST)
        if form.is_valid():
            if not form.cleaned_data['ranged_show']:
                queryset = Transaction.objects.filter(customer=request.user,
                                                      opposite_transaction__isnull=False,
                                                      status=Status.SUCCESS,
                                                      opposite_transaction__status=Status.SUCCESS)
            else:
                queryset = Transaction.objects.filter(customer=request.user,
                                                      completion_date__gte=form.cleaned_data['range_start'],
                                                      completion_date__lte=form.cleaned_data['range_end'],
                                                      opposite_transaction__isnull=False,
                                                      status=Status.SUCCESS,
                                                      opposite_transaction__status=Status.SUCCESS)
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
            final = sell_sum - buy_sum
            return render(request, 'exchange/profitandloss.html', {'form': form,
                                                                   'table': table,
                                                                   'final': final})
    else:
        form = ProfitAndLossForm()
        table = TransactionTable(Transaction.objects.filter(customer=request.user))
        return render(request, 'exchange/profitandloss.html', {'form': form,
                                                               'table': table,
                                                               'final': 'Please specify range to Calculate Profit and Loss'})


def orderbooks_view(request):
    if not request.user.is_authenticated:
        return HttpResponse('Please login first...')
    if request.method == 'POST':
        form = ChoiceExchangeForm(request.POST)
        if form.is_valid():
            coin = form.cleaned_data['currency']
            bids = cache.get(str(coin).upper() + "bids")
            asks = cache.get(str(coin).upper() + "asks")
            bids_table = BidsTable(bids)
            asks_table = AsksTable(asks)
            return render(request, 'exchange/orderbooks.html', {'form': form,
                                                                'bids_table': bids_table,
                                                                'asks_table': asks_table, })
    else:
        form = ChoiceExchangeForm()
        return render(request, 'exchange/orderbooks.html', {'form': form})
